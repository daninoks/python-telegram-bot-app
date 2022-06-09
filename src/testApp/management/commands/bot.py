from django.core.management.base import BaseCommand
from django.conf import settings

from testApp.models import Profile
from testApp.models import Message
from telegram import (
    Bot,
    Update,
)
from telegram.ext import (
    CallbackContext,
    Filters,
    MessageHandler,
    CommandHandler,
    Updater,
)
from telegram.utils.request import Request


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args,**kwargs)
        except Exception as e:
            error_message = f'An error has occurred: {e}'
            print(error_message)
            raise # -*- coding: utf-8 -*-
    return inner


@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )
    m = Message(
        profile=p,
        text=text,
    )
    m.save()

    reply_text = f'Your ID = {chat_id}\nMessage ID = {m.pk}\n{text}'
    update.message.reply_text(
        text=reply_text,
    )


@log_errors
def do_count(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )

    count = Message.objects.filter(profile=p).count()
    # test1 = admin.site.site_header

    update.message.reply_text(
        text=f'You have {count} messages\n\n',
    )


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        # Connection:
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0
            )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
            # base_url=settings.PROXY_URL,
        )
        print(bot.get_me())

        # Updater:
        updater = Updater(
            bot=bot,
            use_context=True,
        )

        message_handler2 = CommandHandler('count', do_count)
        updater.dispatcher.add_handler(message_handler2)

        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)

        # long_polling
        updater.start_polling()
        updater.idle()
