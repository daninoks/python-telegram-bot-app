from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# from testApp.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON
# from testApp.handlers.onboarding.static_text import instruction_button_text, secret_level_button_text

instruction_button_text = 'Инструкция для участников'
leave_sugestion_button_text = 'Оставить предложение'
presentation_button_text = 'PDF-презентация'


def make_keyboard_for_start_command() -> InlineKeyboardMarkup:
    buttons = [
        [
        InlineKeyboardButton(instruction_button_text, url="https://telegra.ph/Instrukcii-dlya-uchastnikov-Dahub-DAO-04-19")
        ],
        [
        InlineKeyboardButton(leave_sugestion_button_text, url="https://docs.google.com/forms/d/e/1FAIpQLSdHEV-BGZXdZrrIGkRHSYU3vI3Fe49MRX8Y_esNFUIbULYUSg/viewform")
        ],
        [
        InlineKeyboardButton(presentation_button_text, url="https://drive.google.com/file/d/1Y6Y75EeXHMhhkxSbigd_dL5holBfO0If/view?usp=sharing")
        ],
    ]
    return InlineKeyboardMarkup(buttons)
