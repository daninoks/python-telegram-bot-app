from typing import Dict




    ##### BUTTONS TEXT #####
support_button_text: Dict[str, str] = {
    'en': 'Contact support',
    'ru': 'Написать в поддержку'
}

instruction_button_text: Dict[str, str] = {
    'en': 'Instruction for members',
    'ru': 'Инструкция для участников'
}

leave_sugestion_button_text: Dict[str, str] = {
    'en': 'Leave an offer',
    'ru':'Оставить предложение'
}

presentation_button_text: Dict[str, str] = {
    'en': 'PDF-presentation',
    'ru': 'PDF-презентация'
}

back_button_text: Dict[str, str] = {
    'en': 'Back',
    'ru': 'Назад'
}


    ##### BUTTONS URLS #####
instruction_button_url = "https://telegra.ph/Instrukcii-dlya-uchastnikov-Dahub-DAO-04-19"

leave_sugestion_button_url = "https://docs.google.com/forms/d/e/1FAIpQLSdHEV-BGZXdZrrIGkRHSYU3vI3Fe49MRX8Y_esNFUIbULYUSg/viewform"

presentation_button_url = "https://drive.google.com/file/d/1Y6Y75EeXHMhhkxSbigd_dL5holBfO0If/view?usp=sharing"


    ##### MESSAGES TEXT #####
start_created: Dict[str, str] = {
    'en': 'Sup, {first_name}!',
    'ru': 'Приветствую, {first_name}!'
}

start_not_created: Dict[str, str] = {
    'en': 'Welcome back, {first_name}!',
    'ru': 'С возвращением, {first_name}!'
}

support_conversation_start: Dict[str, str] = {
    'en': 'Enter your question and click send.',
    'ru': 'Введите ваше обращение и нажмите отправить.'
}

redirect_message_forwarding_body: Dict[str, str] = {
    'en': '{update_to_text}\n\n' \
            '<i>{first_name}</i> <i>{last_name}</i>\n' \
            '(#ID{user_id}) @{username}\n '\
            '<tg-spoiler>request ticket>>{in_bot_mess_id}</tg-spoiler>',
    'ru': '{update_to_text}\n\n' \
            '<i>{first_name}</i> <i>{last_name}</i>\n' \
            '(#ID{user_id}) @{username}\n '\
            '<tg-spoiler>request ticket>>{in_bot_mess_id}</tg-spoiler>'
}

redirect_message_delivery_mess: Dict[str, str] = {
    'en': '{first_name},\n' \
            'Your message has been delivered to the support service.\n' \
            'Experts will answer you very soon!\n\n' \
            'Wait for a response or create another support thread with support - using the text input line',
    'ru': '{first_name},\n' \
            'Ваше сообщение доставлено в службу поддерки.\n' \
            'Специалисты ответят Вам совсем скоро!\n\n' \
            'Дождитесь ответа или создайте еще один сапорт-тред с поддеркой - используя строку ввода текста'
}

redirect_reply_forwarding_body: Dict[str, str] = {
    'en': '{text}\n\n' \
        'To continue the dialogue - reply to this message.\n' \
        '<tg-spoiler>request ticket>>{new_ticket}</tg-spoiler>',
    'ru': '{text}\n\n' \
        'Чтобы продожить диалог - ответьте на это сообщение.\n' \
        '<tg-spoiler>request ticket>>{new_ticket}</tg-spoiler>'
}

forbidden_own_reply: Dict[str, str] = {
    'en': 'You cant reply on Your own and system messages.\n' \
                'Please send regular message or answer existing ticket',
    'ru': 'Вы не можете отвечать на свои собсвенные и систеные сообщения.\n' \
                'Пожалуйста отправьте обычное сообщение или ответьте на существующее обращение'
}
