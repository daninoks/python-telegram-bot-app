from typing import Dict




    ##### VARS TEXT #####
command_ban = '/ban'
command_unban = '/unban'

    ##### BUTTONS TEXT #####

    ##### BUTTONS URLS #####

    ##### MESSAGES TEXT #####
only_for_admins: Dict[str, str] = {
    'en': 'Sorry, this function is available only for admins. Set "admin" flag in django admin panel.',
    'ru': 'Извините, эта функция доступна только для администраторов. Установите флаг «admin» в панели администратора django.'
}

secret_admin_commands: Dict[str, str] = {
    'en': '⚠️ Secret Admin commands:\n' \
            f'{command_ban} @username - ban user from support\n' \
            f'{command_unban} @username - unban user from support',
    'ru': '⚠️ Secret Admin commands:\n' \
            f'{command_ban} @username - забанить Юзера в боте\n' \
            f'{command_unban} @username - забанить Юзера в боте'
}
