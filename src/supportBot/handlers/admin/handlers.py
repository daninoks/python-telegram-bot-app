import re

from supportBot.models import User
from supportBot.handlers.admin import static_text

from telegram import Update
from telegram.ext import CallbackContext



def command_admin(update: Update, context: CallbackContext) -> None:
    """ Show help info about all secret admins commands """
    u = User.get_user(update, context)
    if not u.is_admin:
        update.message.reply_text(static_text.only_for_admins[u.language_code])
        return
    update.message.reply_text(static_text.secret_admin_commands[u.language_code])


def command_ban(update: Update, context: CallbackContext) -> None:
    """
    Ban selected user.
    Usage: /ban @username
    """
    u = User.get_user(update, context)
    if not u.is_admin:
        update.message.reply_text(static_text.only_for_admins[u.language_code])
    else:
        text = update.message.text
        try:
            username = re.findall('@.*', text)[-1]
            target_u = User.set_banned_true(username)
            update.message.reply_text(f"{username} BANNED")

        except Exception as e:
            update.message.reply_text(static_text.secret_admin_commands[u.language_code])
            print('---> exception in command_ban handled')
            print(e)

def command_unban(update: Update, context: CallbackContext) -> None:
    """
    Ban selected user.
    Usage: /unban @username
    """
    u = User.get_user(update, context)
    if not u.is_admin:
        update.message.reply_text(static_text.only_for_admins[u.language_code])
    else:
        text = update.message.text
        try:
            username = re.findall('@.*', text)[-1]
            target_u = User.set_banned_false(username)
            update.message.reply_text(f"{username} UNbanned")

        except Exception as e:
            update.message.reply_text(static_text.secret_admin_commands[u.language_code])
            print('---> exception in command_unban handled')
            print(e)
