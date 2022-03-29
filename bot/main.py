import telebot

import config
from bot.call_types import CallTypes
from bot import commands, handlers

from backend.models import BotUser


bot = telebot.TeleBot(
    token=config.TOKEN,
    num_threads=3,
    parse_mode='HTML',
)


message_handlers = {
    '/start': commands.start_command_handler,
}

key_handlers = {

}


state_handlers = {

}


@bot.message_handler()
def message_handler(message):
    chat_id = message.chat.id
    if not BotUser.users.filter(chat_id=chat_id).exists():
        commands.start_command_handler(bot, message)
        return

    user = BotUser.users.get(chat_id=chat_id)
    if user.bot_state:
        for state, handler in state_handlers.items():
            if state == user.bot_state:
                handler(bot, message)
                break

    for text, handler in message_handlers.items():
        if message.text.startswith(text):
            handler(bot, message)
            break

    for key, handler in key_handlers.items():
        if message.text in key.body:
            handler(bot, message)
            break


callback_query_handlers = {
    CallTypes.Earn: handlers.earn_callback_query_handler,
    CallTypes.GetBonus: handlers.get_bonus_callback_query_handler,
    CallTypes.Profile: handlers.profile_callback_query_handler,
    CallTypes.Menu: handlers.menu_callback_query_handler,
    CallTypes.FundWithdrawal: handlers.fund_withdrawal_callback_query_handler,
    CallTypes.Referals: handlers.referals_callback_query_handler,
    CallTypes.Statistics: handlers.statistics_callback_query_handler,
    CallTypes.Finish: handlers.finish_callback_query_handler,
    CallTypes.Support: handlers.support_callback_query_handler,
}


@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
    call_type = CallTypes.parse_data(call.data)
    for CallType, handler in callback_query_handlers.items():
        if CallType == call_type.__class__:
            handler(bot, call)
            break


if __name__ == "__main__":
    # bot.polling()
    bot.infinity_polling()
