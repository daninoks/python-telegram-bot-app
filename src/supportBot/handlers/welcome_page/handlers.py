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
from supportBot.handlers.utils.info import extract_user_data_from_update
from supportBot.models import User
from supportBot.handlers.welcome_page.keyboards import make_keyboard_for_start_command
from supportBot.handlers.welcome_page import keyboards


def command_start(update: Update, context: CallbackContext) -> None:
    """Handle start command"""
    u, created = User.get_user_and_created(update, context)
    language_code = extract_user_data_from_update(update)['language_code']

    if created:
        text = static_text.start_created[language_code].format(first_name=u.first_name)
    else:
        text = static_text.start_not_created[language_code].format(first_name=u.first_name)

    update.message.reply_text(
        text=text,
        reply_markup=keyboards.make_keyboard_for_start_command(language_code)
    )


def command_start_over(update: Update, context: CallbackContext) -> None:
    """Handle start command"""
    u, created = User.get_user_and_created(update, context)
    language_code = extract_user_data_from_update(update)['language_code']

    if created:
        text = static_text.start_created[language_code].format(first_name=u.first_name)
    else:
        text = static_text.start_not_created[language_code].format(first_name=u.first_name)

    user_id = extract_user_data_from_update(update)['user_id']

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        reply_markup=make_keyboard_for_start_command(language_code),
        parse_mode=ParseMode.HTML
    )


def start_support_conversation_button(update: Update, context: CallbackContext) -> None:
    """Init support dialog"""
    user_id = extract_user_data_from_update(update)['user_id']
    language_code = extract_user_data_from_update(update)['language_code']

    text = static_text.support_conversation_start[language_code]
    back_button_text = static_text.back_button[language_code]

    def make_reply_markup() -> InlineKeyboardMarkup:
        buttons = [
            [
            InlineKeyboardButton(back_button_text, callback_data=f'{BACK_MAINPAGE_BUTTON}')
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
                target_channel_username,
                forwarding_body,
                parse_mode=ParseMode.HTML
            )

            delivery_mess = format(
                f"{first_name},\n" \
                "Ваше сообщение доставлено в службу поддерки.\n" \
                "Специалисты ответят Вам совсем скоро!\n\n" \
                "Дождитесь ответа или создайте еще один сапорт-тред с поддеркой - используя строку ввода текста"

            )
            back_start_button = 'Назад'
            def make_reply_markup() -> InlineKeyboardMarkup:
                buttons = [
                    [
                    InlineKeyboardButton(back_start_button, callback_data=f'{BACK_MAINPAGE_BUTTON}')
                    ],
                ]
                return InlineKeyboardMarkup(buttons)
            context.bot.send_message(
                user_id,
                delivery_mess,
                reply_markup=make_reply_markup(),
                parse_mode=ParseMode.HTML
            )

            # Editing previos InlineKeyboardMarkup:
            prev_message_id = update.message.message_id-1
            try:
                context.bot.edit_message_reply_markup(
                    chat_id=user_id,
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

        forwarding_body = format(
            f"{update.message.text}\n\n" \
            f"Чтобы продожить диалог - ответьте на это сообщение.\n"
            f"<tg-spoiler>request ticket>>{new_ticket}</tg-spoiler>"
        )
        # back_start_button = 'Назад'
        # continue_dialog = 'Ответить'
        #
        # def make_reply_markup() -> InlineKeyboardMarkup:
        #     buttons = [
        #         [
        #         InlineKeyboardButton(back_start_button, callback_data=f'{BACK_MAINPAGE_BUTTON}')
        #         ],
        #         [
        #         InlineKeyboardButton(continue_dialog, callback_data=f'{FORCE_REPLY_BUTTON}')
        #         ],
        #     ]
        #     return InlineKeyboardMarkup(buttons)

        context.bot.send_message(
            user_id,
            f"{forwarding_body}",
            reply_to_message_id = old_ticket,
            reply_markup=ForceReply(
                        force_reply=True,
                        selective=True,
                        input_field_placeholder="Ответьте на сообщение"
                    ),
            parse_mode=ParseMode.HTML
        )
    else:
        """
        Send messages from from BotUser to Discussion tread in Group
        """
        # Need to be moved t oinfo.py:
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
        if bool(re.search('request ticket>>', update.message.reply_to_message.text)) == False:
            self_reply_text = format(
                "You can't reply on Your own and system messages.\n" \
                "Please send regular message or answer existing ticket"
            )
            context.bot.send_message(
                user_id,
                self_reply_text,
                parse_mode=ParseMode.HTML
            )
        else:
            print(update.message.message_id)
            print(update.message.chat.id)
            old_ticket = update.message.reply_to_message.text.split('request ticket>>')[-1]
            new_ticket = update.message.message_id

            forwarding_body = format(
                f"{update.message.text}\n\n" \
                f"<i>{first_name}</i> <i>{last_name}</i>\n" \
                f"(#ID{user_id}) @{username}\n" \
                f"<tg-spoiler>request ticket>>{new_ticket}</tg-spoiler>"
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
                        chat_id=int(user_id),
                        message_id=int(prev_message_id),
                        reply_markup=None,
                    )
                except Exception as e:
                    print('---> exception in redirect_reply_back() handled')
                    print(e)
                    pass

            delivery_mess = format(
                "Ваше сообщение доставлено в службу поддерки.\n" \
                "Специалисты ответят Вам совсем скоро!\n\n" \
                "Дождитесь ответа или создайте еще один сапорт-тред с поддеркой - используя строку ввода текста"

            )
            back_start_button = 'Назад'
            def make_reply_markup() -> InlineKeyboardMarkup:
                buttons = [
                    [
                    InlineKeyboardButton(back_start_button, callback_data=f'{BACK_MAINPAGE_BUTTON}')
                    ],
                ]
                return InlineKeyboardMarkup(buttons)
            context.bot.send_message(
                user_id,
                f"{delivery_mess}",
                reply_to_message_id = old_ticket,
                reply_markup=make_reply_markup(),
                parse_mode=ParseMode.HTML
            )
