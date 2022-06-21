from django.shortcuts import render

import json
import requests

import os
from dotenv import load_dotenv
from pathlib import Path

from django.http import JsonResponse
from django.views import View

# from .models import tb_tutorial_collection
from .models import (
    Profile,
    Message,
)

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    Bot,
    BotCommand,
)
from telegram.ext import (
    Application,
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    ContextTypes,
)

# from testApp.management.commands.hardcode import add_queue
from queue import Queue
# from threading import Thread


dotenv_path = Path('../django_project/.env')
load_dotenv(dotenv_path=dotenv_path)


TELEGRAM_URL = "https://api.telegram.org/bot"
# TUTORIAL_BOT_TOKEN = '5497164468:AAEhn_kbJz-y0UDgWghSzlj8ktNsjmOUf3A'
TUTORIAL_BOT_TOKEN = os.getenv('TOKEN')
# os.getenv("TOKEN", "error_token")
# print(TUTORIAL_BOT_TOKEN)
# print(os.getenv("TOKEN"))
# print(env('TOKEN'))
# TUTORIAL_BOT_TOKEN = "5497164468:AAEhn_kbJz-y0UDgWghSzlj8ktNsjmOUf3A"

# https://api.telegram.org/bot<token>/setWebhook?url=<url>/webhooks/tutorial/
# https://api.telegram.org/bot5497164468:AAEhn_kbJz-y0UDgWghSzlj8ktNsjmOUf3A/setWebhook?url=http://194.67.74.48/webhook/


class TutorialBotView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"ok": "GET request processed"})

    def post(self, request, *args, **kwargs):
        # f = open('/home/django/django_venv/src/post_log', 'a')
        # f.write(request.body)
        # f.close()

        t_data = json.loads(request.body)
        if 'message' in t_data:
            t_message = t_data["message"]
            t_chat = t_message["chat"]
            t_username = t_chat["username"]
            t_id = t_chat["id"]
        else:
            t_message = 'empty'
            t_chat = 'empty'
            t_username = 'empty'
            t_id = 3206063

        # json_request_store(request)

        # add_queue(t_data)
        # text = text.lstrip("/")
        # chatIDtmp = t_data["message"]["chat"]["id"]
        # msg = request.body

        # ### msg = f"{t_data}" + f"HELLODUDE2222\n\n"

        #### self.send_message(msg, t_id)

        # chat = tb_tutorial_collection.find_one({"chat_id": t_chat["id"]})
        # if not chat:
        #     chat = {
        #         "chat_id": t_chat["id"],
        #         "counter": 0
        #     }
        #     response = tb_tutorial_collection.insert_one(chat)
        #     # we want chat obj to be the same as fetched from collection
        #     chat["_id"] = response.inserted_id

        # if text == "+":
        #     chat["counter"] += 1
        #     tb_tutorial_collection.save(chat)
        #     msg = f"Number of '+' messages that were parsed: {chat['counter']}"
        #     self.send_message(msg, t_chat["id"])
        # elif text == "restart":
        #     blank_data = {"counter": 0}
        #     chat.update(blank_data)
        #     tb_tutorial_collection.save(chat)
        #     msg = "The Tutorial bot was restarted"
        #     self.send_message(msg, t_chat["id"])
        # else:
        #     msg = "Unknown command"
        #     self.send_message(msg, t_chat["id"])

        return JsonResponse({"ok": "POST request processed"})

    @staticmethod
    def send_message(message, chat_id):
        # keyboard = [
        #     [InlineKeyboardButton("Log In", callback_data=str("log_in"))],
        # ]
        # reply_markup = InlineKeyboardMarkup(keyboard)
        reply_markup1 = "133313131323425342563245\n\n" + message
        keyboard = {
            "inline_keyboard": [[
                {
                    "text": "A",
                    "callback_data": "A1"
                },
                {
                    "text": "B",
                    "callback_data": "C1"
                }
            ]]
        }
        # "parse_mode": "Markdown",
        #             "reply_markup": reply_markup,
        data = {
            "chat_id": chat_id,
            "text": reply_markup1,
            "reply_markup": json.dumps(keyboard),
            "parse_mode": "Markdown",
        }
        response = requests.post(
            f"{TELEGRAM_URL}{TUTORIAL_BOT_TOKEN}/sendMessage", data=data
        )
