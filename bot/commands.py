from telebot import TeleBot, types

from backend.templates import Messages, Keys
from backend.models import BotUser

from bot.call_types import CallTypes
from bot import utils


def start_command_handler(bot: TeleBot, message):
    chat_id = message.chat.id
    bot.send_message(chat_id, Messages.START_MESSAGE_HANDLER)

    if not BotUser.users.filter(chat_id=chat_id).exists():
        username = message.chat.username
        full_name = message.chat.first_name
        if message.chat.last_name:
            full_name += ' ' + message.chat.last_name

        BotUser.users.create(full_name=full_name,
                             username=username,
                             chat_id=chat_id)

    if len(data := message.text.split()) == 2:
        referal_chat_id = data[-1]
        user = BotUser.users.get(chat_id=chat_id)
        if referal_chat_id != user.chat_id:
            user_referal = BotUser.users.get(chat_id=referal_chat_id)
            user_referal.referals.add(user)

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
    keyboard.add(support_button)
    user = BotUser.users.get(chat_id=chat_id)
    if user.is_admin:
        statistics_button = utils.make_inline_button(
            text=Keys.STATISTICS,
            CallType=CallTypes.Statistics,
        )
        keyboard.add(statistics_button)

    text = utils.text_to_fat(Messages.MENU)
    bot.send_message(chat_id, text,
                     reply_markup=keyboard)
