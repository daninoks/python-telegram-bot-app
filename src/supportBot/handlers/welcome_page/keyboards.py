from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from supportBot.handlers.welcome_page.manage_data import SUPPORT_BUTTON
from supportBot.handlers.welcome_page import static_text




def make_keyboard_for_start_command(language_code) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                static_text.support_button_text[language_code],
                callback_data=f'{SUPPORT_BUTTON}'
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
