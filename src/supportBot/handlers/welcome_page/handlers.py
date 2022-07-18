from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from supportBot.handlers.welcome_page.manage_data import BACK_MAINPAGE_BUTTON

import datetime

import re
import json

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from supportBot.handlers.welcome_page import static_text
from supportBot.handlers.utils.info import extract_user_data_from_update
from supportBot.models import User
from supportBot.handlers.welcome_page.keyboards import make_keyboard_for_start_command


def command_start(update: Update, context: CallbackContext) -> None:
    """Handle start command"""
    u, created = User.get_user_and_created(update, context)

    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)

    update.message.reply_text(text=text,
                              reply_markup=make_keyboard_for_start_command())


def command_start_over(update: Update, context: CallbackContext) -> None:
    """Handle start command"""
    u, created = User.get_user_and_created(update, context)

    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)

    user_id = extract_user_data_from_update(update)['user_id']

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        reply_markup=make_keyboard_for_start_command(),
        parse_mode=ParseMode.HTML
    )


def start_support_conversation_button(update: Update, context: CallbackContext) -> None:
    """Init support dialog"""
    user_id = extract_user_data_from_update(update)['user_id']
    text = format("Введите сообщение.\n" \
                  "Специалисты поддерки ответят вам совсем скоро!")
    back_start_button = 'Назад'
    def make_reply_markup() -> InlineKeyboardMarkup:
        buttons = [
            [
            InlineKeyboardButton(back_start_button, callback_data=f'{BACK_MAINPAGE_BUTTON}')
            ],
        ]
        return InlineKeyboardMarkup(buttons)

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        reply_markup=make_reply_markup(),
        parse_mode=ParseMode.HTML
    )


def redirect_message_to_channel(update: Update, context: CallbackContext) -> None:
    """Redirect any message contain chars from users"""
    # Channel where messages will redirect:
    target_chat_username = "@WWUNDERGROUND"

    if update.message.chat.username is not None:
        update_dict = extract_user_data_from_update(update)
        user_id = update_dict['user_id']
        username = update_dict['username']

        if 'first_name' in update_dict.keys():
            first_name = update_dict['first_name']
        else:
            first_name = ""
        if 'last_name' in update_dict.keys():
            last_name = update_dict['last_name']
        else:
            last_name = ""

        # update_to_text = dir(update.message.chat.username)
        # update_to_text = update.message.chat.username
        update_to_text = update.message.text
        in_bot_mess_id = update.message.message_id

        forwarding_body = format(
            f"{update_to_text}\n" \
            f"\n" \
            f"<i>{first_name}</i> <i>{last_name}</i>\n" \
            f"(#ID{user_id}) @{username}\n" \
            f"<tg-spoiler>request ticket>>{in_bot_mess_id}</tg-spoiler>"
        )

        context.bot.send_message(
            target_chat_username,
            forwarding_body,
            parse_mode=ParseMode.HTML
        )


def redirect_reply_back(update: Update, context: CallbackContext) -> None:
    """Redirects reply from channel/discussion back to bot dialog"""

    try:
        """Send messages from Replies Group to BotUser"""
        if update.message.sender_chat.type is not None:
            old_ticket = update.message.reply_to_message.text.split('request ticket>>')[-1]
            new_ticket = update.message.message_id
            forwarding_body = format(f"{update.message.text}\n\n" \
                            f"<tg-spoiler>request ticket>>{new_ticket}</tg-spoiler>"
            )

            context.bot.send_message(
                3206063,
                f"{forwarding_body}",
                reply_to_message_id = old_ticket,
                parse_mode=ParseMode.HTML
            )
    except:
        """Send messages from from BotUser to Discussion tread in Group"""
        target_chat_username = "@WWUChat"

        if update.message.chat.username is not None:
            update_dict = extract_user_data_from_update(update)
            user_id = update_dict['user_id']
            username = update_dict['username']

            if 'first_name' in update_dict.keys():
                first_name = update_dict['first_name']
            else:
                first_name = ""
            if 'last_name' in update_dict.keys():
                last_name = update_dict['last_name']
            else:
                last_name = ""

        old_ticket = update.message.reply_to_message.text.split('request ticket>>')[-1]
        new_ticket = update.message.message_id
        forwarding_body = format( f"{update.message.text}\n\n" \
                        f"<i>{first_name}</i> <i>{last_name}</i>\n" \
                        f"(#ID{user_id}) @{username}\n" \
                        f"<tg-spoiler>request ticket>>{new_ticket}</tg-spoiler>"
        )

        context.bot.send_message(
            target_chat_username,
            f"{forwarding_body}",
            reply_to_message_id = old_ticket,
            parse_mode=ParseMode.HTML
        )
