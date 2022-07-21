from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from supportBot.handlers.welcome_page import static_text
from supportBot.handlers.welcome_page import manage_data




def make_keyboard_for_start_command(language_code) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                static_text.support_button_text[language_code],
                callback_data=manage_data.SUPPORT_BUTTON
            )
        ],
        [
            InlineKeyboardButton(
                static_text.instruction_button_text[language_code],
                url=static_text.instruction_button_url
            )
        ],
        [
            InlineKeyboardButton(
                static_text.leave_sugestion_button_text[language_code],
                url=static_text.leave_sugestion_button_url
            )
        ],
        [
            InlineKeyboardButton(
                static_text.presentation_button_text[language_code],
                url=static_text.presentation_button_url
            )
        ],
    ]
    return InlineKeyboardMarkup(buttons)

def make_keyboard_for_support_conversation(language_code) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                static_text.back_button_text[language_code],
                callback_data=manage_data.BACK_MAINPAGE_BUTTON
            )
        ],
    ]
    return InlineKeyboardMarkup(buttons)
