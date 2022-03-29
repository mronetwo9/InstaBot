from telebot import TeleBot, types

from backend.models import (BONUS_VALUE, PAYMENT_PERMS_REFERALS_COUNT,
                            PAYMENT_PERMS_VIEWED_VIDEOS_COUNT, BotUser,
                            ViewVideo, Video)
from backend.templates import Keys, Messages

from bot import utils
from bot.call_types import CallTypes


def menu_callback_query_handler(bot: TeleBot, call):
    chat_id = call.message.chat.id
    user = BotUser.users.get(chat_id=chat_id)
    earn_button = utils.make_inline_button(
        text=Keys.EARN,
        CallType=CallTypes.Earn,
    )
    profile_button = utils.make_inline_button(
        text=Keys.PROFILE,
        CallType=CallTypes.Profile,
    )
    fund_withdrawal_button = utils.make_inline_button(
        text=Keys.FUND_WITHDRAWAL,
        CallType=CallTypes.FundWithdrawal,
    )
    referals_button = utils.make_inline_button(
        text=Keys.REFERALS,
        CallType=CallTypes.Referals,
    )
    support_button = utils.make_inline_button(
        text=Keys.SUPPORT,
        CallType=CallTypes.Support,
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(earn_button)
    keyboard.add(profile_button)
    keyboard.add(fund_withdrawal_button)
    keyboard.add(referals_button)
    if user.is_admin:
        statistics_button = utils.make_inline_button(
            text=Keys.STATISTICS,
            CallType=CallTypes.Statistics,
        )
        keyboard.add(statistics_button)

    keyboard.add(support_button)
    text = utils.text_to_fat(Messages.MENU)
    bot.edit_message_text(
        chat_id=chat_id,
        text=text,
        message_id=call.message.id,
        reply_markup=keyboard,
    )


def earn_callback_query_handler(bot: TeleBot, call):
    chat_id = call.message.chat.id
    user: BotUser = BotUser.users.get(chat_id=chat_id)
    if not user.check_video_limit_per_day():
        text = Messages.VIDEOS_PER_DAY_LIMIT_EXCEEDED
        bot.send_message(chat_id, text)
        return

    video = user.get_next_video()
    view_video = ViewVideo.objects.create(
        user=user,
        video=video,
    )
    bot.delete_message(chat_id, call.message.id)
    get_bonus_button = utils.make_inline_button(
        text=Keys.GET_BONUS.format(
            bonus=utils.get_money_value_text(BONUS_VALUE)
        ),
        CallType=CallTypes.GetBonus,
        id=view_video.id,
    )
    finish_button = utils.make_inline_button(
        text=Keys.FINISH,
        CallType=CallTypes.Finish,
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(get_bonus_button)
    keyboard.add(finish_button)

    bot.send_video(
        chat_id=chat_id,
        video=video.get_data(),
        reply_markup=keyboard,
    )


def get_bonus_callback_query_handler(bot: TeleBot, call):
    chat_id = call.message.chat.id
    user: BotUser = BotUser.users.get(chat_id=chat_id)
    call_type = CallTypes.parse_data(call.data)
    view_video_id = call_type.id
    view_video: ViewVideo = ViewVideo.objects.get(id=view_video_id)
    if view_video.received:
        return

    if view_video.can_get_bonus():
        bot.delete_message(chat_id, call.message.id)
        view_video.received = True
        view_video.save()
        user.balance += BONUS_VALUE
        user.save()
        see_more_button = utils.make_inline_button(
            text=Keys.SEE_MORE,
            CallType=CallTypes.Earn,
        )
        finish_button = utils.make_inline_button(
            text=Keys.FINISH,
            CallType=CallTypes.Finish,
        )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(see_more_button)
        keyboard.add(finish_button)
        text = Messages.BONUS_RECEIVED.format(
            balance=utils.get_money_value_text(user.balance),
            videos_count=user.get_today_viewed_videos().count(),
        )
        bot.send_message(chat_id, text,
                         reply_markup=keyboard)
    else:
        text = Messages.NOT_SO_FAST
        bot.answer_callback_query(call.id, text, show_alert=True)


def finish_callback_query_handler(bot: TeleBot, call):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.id)
    user: BotUser = BotUser.users.get(chat_id=chat_id)
    text = Messages.PROFILE.format(
        first_name=call.message.chat.first_name,
        username=call.message.chat.username,
        balance=utils.get_money_value_text(user.balance),
        referals_count=user.referals.count(),
        true_referals_count=user.get_true_referals().count(),
        videos_count=user.videos.count(),
        videos_count_today=user.get_today_viewed_videos().count(),
    )
    earn_button = utils.make_inline_button(
        text=Keys.EARN,
        CallType=CallTypes.Earn,
    )
    fund_withdrawal_button = utils.make_inline_button(
        text=Keys.FUND_WITHDRAWAL,
        CallType=CallTypes.FundWithdrawal,
    )
    referals_button = utils.make_inline_button(
        text=Keys.REFERALS,
        CallType=CallTypes.Referals,
    )
    menu_button = utils.make_inline_button(
        text=Keys.MENU,
        CallType=CallTypes.Menu,
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(earn_button)
    keyboard.add(fund_withdrawal_button)
    keyboard.add(referals_button)
    keyboard.add(menu_button)
    bot.send_message(
        text=text,
        chat_id=chat_id,
        reply_markup=keyboard,
    )


def profile_callback_query_handler(bot: TeleBot, call):
    chat_id = call.message.chat.id
    user: BotUser = BotUser.users.get(chat_id=chat_id)
    text = Messages.PROFILE.format(
        first_name=call.message.chat.first_name,
        username=call.message.chat.username,
        balance=utils.get_money_value_text(user.balance),
        referals_count=user.referals.count(),
        true_referals_count=user.get_true_referals().count(),
        videos_count=user.videos.count(),
        videos_count_today=user.get_today_viewed_videos().count(),
    )
    earn_button = utils.make_inline_button(
        text=Keys.EARN,
        CallType=CallTypes.Earn,
    )
    fund_withdrawal_button = utils.make_inline_button(
        text=Keys.FUND_WITHDRAWAL,
        CallType=CallTypes.FundWithdrawal,
    )
    referals_button = utils.make_inline_button(
        text=Keys.REFERALS,
        CallType=CallTypes.Referals,
    )
    menu_button = utils.make_inline_button(
        text=Keys.MENU,
        CallType=CallTypes.Menu,
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(earn_button)
    keyboard.add(fund_withdrawal_button)
    keyboard.add(referals_button)
    keyboard.add(menu_button)
    bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=call.message.id,
        reply_markup=keyboard,
    )


def fund_withdrawal_callback_query_handler(bot: TeleBot, call):
    chat_id = call.message.chat.id
    user: BotUser = BotUser.users.get(chat_id=chat_id)
    true_referals_count = user.get_true_referals().count()
    videos_count = user.videos.count()
    done_1 = true_referals_count >= PAYMENT_PERMS_REFERALS_COUNT
    done_2 = videos_count >= PAYMENT_PERMS_VIEWED_VIDEOS_COUNT
    smiles = ['❌', '✅']
    text = Messages.FUND_WITHDRAWAL.format(
        true_referals_count=true_referals_count,
        true_referals_count_required=PAYMENT_PERMS_REFERALS_COUNT,
        true_referals_count_done=smiles[done_1],
        videos_count=videos_count,
        videos_count_required=PAYMENT_PERMS_VIEWED_VIDEOS_COUNT,
        videos_count_done=smiles[done_2],
    )
    watch_video_button = utils.make_inline_button(
        text=Keys.WATCH_VIDEO,
        CallType=CallTypes.Earn,
    )
    referals_button = utils.make_inline_button(
        text=Keys.REFERALS,
        CallType=CallTypes.Referals,
    )
    menu_button = utils.make_inline_button(
        text=Keys.MENU,
        CallType=CallTypes.Menu,
    )
    keyboard = types.InlineKeyboardMarkup()
    if done_1 and done_2:
        get_paid_button = utils.make_inline_button(
            text=Keys.GET_PAID,
            CallType=CallTypes.GetPaid,
        )
        keyboard.add(get_paid_button)

    keyboard.add(watch_video_button)
    keyboard.add(referals_button)
    keyboard.add(menu_button)
    bot.edit_message_text(
        chat_id=chat_id,
        text=text,
        message_id=call.message.id,
        reply_markup=keyboard,
    )


def referals_callback_query_handler(bot: TeleBot, call):
    chat_id = call.message.chat.id
    user: BotUser = BotUser.users.get(chat_id=chat_id)
    referals_info = str()
    for index, referal in enumerate(user.referals.all(), 1):
        referal_info = Messages.REFERAL.format(
            index=index,
            chat_id=referal.chat_id,
            full_name=referal.full_name,
            videos_count=referal.videos.count(),
        )
        referals_info += referal_info + '\n'

    text = utils.text_to_fat(Keys.REFERALS)
    text += utils.text_to_double_line(referals_info)
    referal_link = f't.me/watchvideoearnbot?start={user.chat_id}'
    text += Messages.REFERAL_LINK.format(
        referal_link=utils.text_to_code(referal_link),
    )
    watch_video_button = utils.make_inline_button(
        text=Keys.WATCH_VIDEO,
        CallType=CallTypes.Earn,
    )
    fund_withdrawal_button = utils.make_inline_button(
        text=Keys.FUND_WITHDRAWAL,
        CallType=CallTypes.FundWithdrawal,
    )
    menu_button = utils.make_inline_button(
        text=Keys.MENU,
        CallType=CallTypes.Menu,
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(watch_video_button)
    keyboard.add(fund_withdrawal_button)
    keyboard.add(menu_button)
    bot.edit_message_text(
        chat_id=chat_id,
        text=text,
        message_id=call.message.id,
        reply_markup=keyboard,
    )


def support_callback_query_handler(bot: TeleBot, call):
    chat_id = call.message.chat.id
    text = Messages.SUPPORT
    earn_button = utils.make_inline_button(
        text=Keys.EARN,
        CallType=CallTypes.Earn,
    )
    menu_button = utils.make_inline_button(
        text=Keys.MENU,
        CallType=CallTypes.Menu,
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(earn_button)
    keyboard.add(menu_button)
    bot.edit_message_text(
        chat_id=chat_id,
        text=text,
        message_id=call.message.id,
        reply_markup=keyboard,
    )


def statistics_callback_query_handler(bot: TeleBot, call):
    chat_id = call.message.chat.id
    text = Messages.STATISTICS.format(
        users_count=BotUser.users.count(),
        videos_count=Video.videos.count(),
        video_views_count=ViewVideo.objects.count(),
    )
    earn_button = utils.make_inline_button(
        text=Keys.EARN,
        CallType=CallTypes.Earn,
    )
    menu_button = utils.make_inline_button(
        text=Keys.MENU,
        CallType=CallTypes.Menu,
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(earn_button)
    keyboard.add(menu_button)
    bot.edit_message_text(
        chat_id=chat_id,
        text=text,
        message_id=call.message.id,
        reply_markup=keyboard,
    )
