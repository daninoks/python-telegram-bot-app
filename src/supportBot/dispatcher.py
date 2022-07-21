"""
    Telegram event handlers
"""
import sys
import logging
from typing import Dict

import telegram.error
from telegram import Bot, Update, BotCommand
from telegram.ext import (
    Updater, Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler, RegexHandler,
)

from django_project.celery import app  # event processing in async mode
from django_project.settings import TELEGRAM_TOKEN_SUPPORT, DEBUG

from supportBot.handlers.utils import error
from supportBot.handlers.welcome_page import handlers as welcome_handlers
from supportBot.handlers.welcome_page.manage_data import SUPPORT_BUTTON
from supportBot.handlers.welcome_page.manage_data import BACK_MAINPAGE_BUTTON
# from testApp.handlers.utils import files,
# from testApp.handlers.admin import handlers as admin_handlers
# # from testApp.handlers.location import handlers as location_handlers
# from testApp.handlers.onboarding import handlers as onboarding_handlers
# from testApp.handlers.broadcast_message import handlers as broadcast_handlers
# from testApp.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON
# from testApp.handlers.broadcast_message.manage_data import CONFIRM_DECLINE_BROADCAST
# from testApp.handlers.broadcast_message.static_text import broadcast_command


def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram.
    """
    # onboarding
    dp.add_handler(CommandHandler("start", welcome_handlers.command_start))
    dp.add_handler(CallbackQueryHandler(welcome_handlers.command_start_over, pattern=f"^{BACK_MAINPAGE_BUTTON}$"))

    # support conversation:
    dp.add_handler(CallbackQueryHandler(welcome_handlers.start_support_conversation_button, pattern=f"^{SUPPORT_BUTTON}$"))


    # Message redirecting (all text passed from input line for now):
    # dp.add_handler(CallbackQueryHandler(welcome_handlers.redirect_message_to_channel, pattern=".*"))
    dp.add_handler(
        MessageHandler(
            Filters.reply, welcome_handlers.redirect_reply_back
        )
    )
    dp.add_handler(
        RegexHandler(
            ".*", welcome_handlers.redirect_message_to_channel
        )
    )


    # admin commands
    # dp.add_handler(CommandHandler("admin", admin_handlers.admin))
    # dp.add_handler(CommandHandler("stats", admin_handlers.stats))
    # dp.add_handler(CommandHandler('export_users', admin_handlers.export_users))

    # # location
    # dp.add_handler(CommandHandler("ask_location", location_handlers.ask_for_location))
    # dp.add_handler(MessageHandler(Filters.location, location_handlers.location_handler))
    #
    # # secret level
    # dp.add_handler(CallbackQueryHandler(onboarding_handlers.secret_level, pattern=f"^{SECRET_LEVEL_BUTTON}"))
    #
    # # broadcast message
    # dp.add_handler(
    #     MessageHandler(Filters.regex(rf'^{broadcast_command}(/s)?.*'), broadcast_handlers.broadcast_command_with_message)
    # )
    # dp.add_handler(
    #     CallbackQueryHandler(broadcast_handlers.broadcast_decision_handler, pattern=f"^{CONFIRM_DECLINE_BROADCAST}")
    # )
    #
    # # files
    # dp.add_handler(MessageHandler(
    #     Filters.animation, files.show_file_id,
    # ))

    # handling errors
    dp.add_error_handler(error.send_stacktrace_to_tg_chat)

    # EXAMPLES FOR HANDLERS
    # dp.add_handler(MessageHandler(Filters.text, <function_handler>))
    # dp.add_handler(MessageHandler(
    #     Filters.document, <function_handler>,
    # ))
    # dp.add_handler(CallbackQueryHandler(<function_handler>, pattern="^r\d+_\d+"))
    # dp.add_handler(MessageHandler(
    #     Filters.chat(chat_id=int(TELEGRAM_FILESTORAGE_ID)),
    #     # & Filters.forwarded & (Filters.photo | Filters.video | Filters.animation),
    #     <function_handler>,
    # ))

    return dp


def run_pooling():
    """
    Get webhook info:
        https://api.telegram.org/bot{my_bot_token}/getWebhookInfo
    Set/Del webhook:
        https://api.telegram.org/bot{my_bot_token}/setWebhook?url={url_to_send_updates_to}
        https://api.telegram.org/bot5497164468:AAEhn_kbJz-y0UDgWghSzlj8ktNsjmOUf3A/setWebhook?url=https://194-67-74-48.cloudvps.regruhosting.ru/webhook/

        https://api.telegram.org/bot{my_bot_token}/deleteWebhook?url={url_to_send_updates_to}
        https://api.telegram.org/bot5497164468:AAEhn_kbJz-y0UDgWghSzlj8ktNsjmOUf3A/deleteWebhook?url=https://194-67-74-48.cloudvps.regruhosting.ru/webhook/
    """

    """ Run bot in pooling mode """
    updater = Updater(TELEGRAM_TOKEN_SUPPORT, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = Bot(TELEGRAM_TOKEN_SUPPORT).get_me()
    bot_link = f"https://t.me/" + bot_info["username"]

    print(f"Pooling of '{bot_link}' started")
    # it is really useful to send '👋' emoji to developer
    # when you run local test
    # bot.send_message(text='👋', chat_id=<YOUR TELEGRAM ID>)

    updater.start_polling()
    updater.idle()


# Global variable - best way I found to init Telegram bot
bot = Bot(TELEGRAM_TOKEN_SUPPORT)
try:
    TELEGRAM_BOT_USERNAME = bot.get_me()["username"]
except telegram.error.Unauthorized:
    logging.error(f"Invalid TELEGRAM_TOKEN.")
    sys.exit(1)


@app.task(ignore_result=True)
def process_telegram_event(update_json):
    update = Update.de_json(update_json, bot)
    dispatcher.process_update(update)


def set_up_commands(bot_instance: Bot) -> None:
    langs_with_commands: Dict[str, Dict[str, str]] = {
        'en': {
            'start': 'Start django bot 🚀',
            'admin': 'Show admin info ℹ️',
        },
        'ru': {
            'start': 'Запустить django бота 🚀',
            'admin': 'Показать информацию для админов ℹ️',
        }
    }

    bot_instance.delete_my_commands()
    for language_code in langs_with_commands:
        bot_instance.set_my_commands(
            language_code=language_code,
            commands=[
                BotCommand(command, description) for command, description in langs_with_commands[language_code].items()
            ]
        )


# WARNING: it's better to comment the line below in DEBUG mode.
# Likely, you'll get a flood limit control error, when restarting bot too often
set_up_commands(bot)

n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))
