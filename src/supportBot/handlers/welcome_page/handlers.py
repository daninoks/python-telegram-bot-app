from supportBot.handlers.welcome_page.manage_data import BACK_MAINPAGE_BUTTON
from supportBot.handlers.welcome_page.manage_data import FORCE_REPLY_BUTTON

import datetime

import re
import json

from django.utils import timezone
from telegram import ParseMode, Update, ForceReply, ReplyKeyboardRemove
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from supportBot.handlers.welcome_page import static_text
from supportBot.handlers.welcome_page import keyboards
from supportBot.handlers.utils.info import extract_user_data_from_update
from supportBot.models import User


def command_start(update: Update, context: CallbackContext) -> None:
    """Handle start command"""
    u, created = User.get_user_and_created(update, context)

    if created:
        text = static_text.start_created[u.language_code].format(first_name=u.first_name)
    else:
        text = static_text.start_not_created[u.language_code].format(first_name=u.first_name)

    update.message.reply_text(
        text=text,
        reply_markup=keyboards.make_keyboard_for_start_command(u.language_code)
    )


def command_start_over(update: Update, context: CallbackContext) -> None:
    """Handle start command"""
    u, created = User.get_user_and_created(update, context)

    if created:
        text = static_text.start_created[u.language_code].format(first_name=u.first_name)
    else:
        text = static_text.start_not_created[u.language_code].format(first_name=u.first_name)

    context.bot.edit_message_text(
        text=text,
        chat_id=u.user_id,
        message_id=update.callback_query.message.message_id,
        reply_markup=keyboards.make_keyboard_for_start_command(u.language_code),
        parse_mode=ParseMode.HTML
    )


def start_support_conversation_button(update: Update, context: CallbackContext) -> None:
    """Init support dialog"""
    u = User.get_user(update, context)

    text = static_text.support_conversation_start[u.language_code]

    context.bot.edit_message_text(
        text=text,
        chat_id=u.user_id,
        message_id=update.callback_query.message.message_id,
        reply_markup=keyboards.make_keyboard_for_support_conversation(u.language_code),
        parse_mode=ParseMode.HTML
    )


def redirect_message_to_channel(update: Update, context: CallbackContext) -> None:
    """
    Redirect (via send_message due privicy reasons) any message contain chars
    from BotUser to target channel (!with preset redirection to group discussion!)
    """
    # Channel where messages will redirect:
    target_channel_username = "@WWUNDERGROUND"
    target_chat_username = "@WWUChat"
    # Make possible to configure targets chats from django admin panel (DB),
    # and via admin panel directly in Bot.

    # Need to be moved t oinfo.py:
    if update.message.chat.username != re.sub('@', '', target_chat_username):
        if update.message.chat.username is not None:
            u = User.get_user(update, context)

            if u.first_name == None:
                first_name = ""
            else:
                first_name = u.first_name
            if u.last_name == None:
                last_name = ""
            else:
                last_name = u.last_name

            # update_to_text = dir(update.message.chat.username)
            update_to_text = update.message.text
            in_bot_mess_id = update.message.message_id

            forwarding_body = static_text.redirect_message_forwarding_body[u.language_code].format(
                update_to_text = update_to_text,
                first_name = first_name,
                last_name = last_name,
                user_id = u.user_id,
                username = u.username,
                in_bot_mess_id = in_bot_mess_id
            )
            context.bot.send_message(
                target_channel_username,
                forwarding_body,
                parse_mode=ParseMode.HTML
            )

            delivery_mess = static_text.redirect_message_delivery_mess[u.language_code].format(
                first_name = first_name
            )

            context.bot.send_message(
                u.user_id,
                delivery_mess,
                reply_markup=keyboards.make_keyboard_for_support_conversation(u.language_code),
                parse_mode=ParseMode.HTML
            )

            # Editing previos InlineKeyboardMarkup:
            prev_message_id = update.message.message_id-1
            try:
                context.bot.edit_message_reply_markup(
                    chat_id=u.user_id,
                    message_id=prev_message_id,
                    reply_markup=None,
                )
            except Exception as e:
                print('---> exception in redirect_message_to_channel() handled')
                print(e)
                pass


def redirect_reply_back(update: Update, context: CallbackContext) -> None:
    """
    Redirects reply from channel-discussion back to bot dialog
    """
    # Channel discussion where messages will redirect:
    target_chat_username = "@WWUChat"

    if update.message.chat.username == re.sub('@', '', target_chat_username):
        """
        Send messages from Replies Group to BotUser
        """
        u = User.get_user(update, context)

        old_ticket = update.message.reply_to_message.text.split('request ticket>>')[-1]
        new_ticket = update.message.message_id
        re_user_id = re.findall('\(#ID.*\)', update.message.reply_to_message.text)[-1]
        user_id = re.findall('\d+', re_user_id)[-1]

        # Editing previos InlineKeyboardMarkup:
        counter=1
        edit_chat_id = int(user_id)
        while counter < 5:
            prev_message_id = int(old_ticket)+counter
            counter+=1
            try:
                context.bot.edit_message_reply_markup(
                    chat_id=int(user_id),
                    message_id=int(prev_message_id),
                    reply_markup=None,
                )
            except Exception as e:
                print('---> exception in redirect_reply_back() handled')
                print(e)
                pass

        forwarding_body = static_text.redirect_reply_forwarding_body[u.language_code].format(
            text = update.message.text,
            new_ticket = new_ticket
        )
        context.bot.send_message(
            int(user_id),
            forwarding_body,
            reply_to_message_id = old_ticket,
            reply_markup=ForceReply(
                        force_reply=True,
                        selective=True,
                        input_field_placeholder=None
                    ),
            parse_mode=ParseMode.HTML
        )
    else:
        """
        Send messages from from BotUser to Discussion tread in Group
        """
        u = User.get_user(update, context)
        if u.first_name == None:
            first_name = ""
        else:
            first_name = u.first_name
        if u.last_name == None:
            last_name = ""
        else:
            last_name = u.last_name

        if bool(re.search('request ticket>>', update.message.reply_to_message.text)) == False:
            self_reply_text =  static_text.forbidden_own_reply[u.language_code]
            context.bot.send_message(
                u.user_id,
                self_reply_text,
                parse_mode=ParseMode.HTML
            )
        else:
            print(update.message.message_id)
            print(update.message.chat.id)
            old_ticket = update.message.reply_to_message.text.split('request ticket>>')[-1]
            new_ticket = update.message.message_id

            forwarding_body = static_text.redirect_message_forwarding_body[u.language_code].format(
                update_to_text = update.message.text,
                first_name = first_name,
                last_name = last_name,
                user_id = u.user_id,
                username = u.username,
                in_bot_mess_id = old_ticket
            )
            context.bot.send_message(
                target_chat_username,
                forwarding_body,
                reply_to_message_id = old_ticket,
                parse_mode=ParseMode.HTML
            )

            # Editing previos InlineKeyboardMarkup:
            counter=1
            while counter < 5:
                prev_message_id = update.message.message_id-counter
                counter+=1
                try:
                    context.bot.edit_message_reply_markup(
                        chat_id=u.user_id,
                        message_id=int(prev_message_id),
                        reply_markup=None,
                    )
                except Exception as e:
                    print('---> exception in redirect_reply_back() handled')
                    print(e)
                    pass

            delivery_mess = static_text.redirect_message_delivery_mess[u.language_code].format(
                first_name = first_name
            )

            context.bot.send_message(
                u.user_id,
                delivery_mess,
                reply_to_message_id = new_ticket,
                reply_markup=keyboards.make_keyboard_for_support_conversation(u.language_code),
                parse_mode=ParseMode.HTML
            )
