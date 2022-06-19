#!/home/django/django_venv/lib64/python3.8

# from telegram import (
#     Bot,
# )
#
# from telegram.ext import (
#     Updater,
# )

from typing import List, Tuple, cast
from telegram import (
    ParseMode,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    Bot,
    BotCommand,
)
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    InvalidCallbackData,
    PicklePersistence,
    Dispatcher,
    MessageHandler
)

from telegram.utils import helpers
import environ
import os


# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

# API_TOKEN = env('TOKEN')
API_TOKEN = '5497164468:AAEhn_kbJz-y0UDgWghSzlj8ktNsjmOUf3A'

FIRST = 1

Bot(API_TOKEN).set_my_commands([
    BotCommand('start', 'start page'),
    BotCommand('test', 'test script'),
])

# COMMANDS FUNCTIONS:
def start(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    print(update)
    print(update.message.chat.id)
    print(up.get_lang(update.message.chat.id))

    # welcome_mess = langMessLib.start_mess(update, up)
    welcome_mess = "RRRRRRRRR"
    # bot = context.bot
    # url = helpers.create_deep_linked_url(
    #     bot.username, 'check-this-out', group=True)

    keyboard = [
        [InlineKeyboardButton("Log In", callback_data=str("LOG_IN"))],
        # [InlineKeyboardButton("Support", callback_data=str(SUPPORT_MENU))],
        # [InlineKeyboardButton("Share Bot", url=url)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text=welcome_mess, reply_markup=reply_markup)
    return FIRST


def main() -> None:
    """Run bot scenario. With JSON response."""
    if 'PORT' in os.environ:
        default_ip = '0.0.0.0'
        default_port = os.environ.get('PORT')
    else:
        default_ip = '127.0.0.1'
        default_port = '8000'

    updater = Updater(API_TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
        ],
        states={
            FIRST: [
                CallbackQueryHandler(
                    start, pattern="^" + str("LOG_IN") + "$"
                ),
            ],
        },
        fallbacks=[
            CommandHandler('start', start),
        ],
    )

    updater.start_webhook(
        listen=default_ip,
        port=default_port,
        url_path=API_TOKEN,
        webhook_url="https://194-67-74-48.cloudvps.regruhosting.ru/webhook/"
    )


if __name__ == '__main__':
    main()
