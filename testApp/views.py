from django.shortcuts import render

import json
import os

import requests
from django.http import JsonResponse
from django.views import View

# from .models import tb_tutorial_collection
from testApp.models import (
    Profile,
    Message,
)

TELEGRAM_URL = "https://api.telegram.org/bot"
TUTORIAL_BOT_TOKEN = '5497164468:AAEhn_kbJz-y0UDgWghSzlj8ktNsjmOUf3A'
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
        t_message = t_data["message"]
        # t_text = t_message["text"]
        t_chat = t_message["chat"]
        t_username = t_chat["username"]
        t_id = t_chat["id"]

        try:
            t_text = t_message["text"].strip().lower()
        except Exception as e:
            return JsonResponse({"ok": "POST request processed"})

        p, _ = Profile.objects.get_or_create(
            external_id=t_id,
            defaults={
                'name': t_username,
            }
        )
        m = Message(
            profile=p,
            text=t_text,
        )
        m.save()



        # text = text.lstrip("/")
        chatIDtmp = t_data["message"]["chat"]["id"]
        # msg = request.body
        msg = f"{t_data}" + f"HELLODUDE\n\n" + f"{t_text}"
        self.send_message(msg, t_chat["id"])
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
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        response = requests.post(
            f"{TELEGRAM_URL}{TUTORIAL_BOT_TOKEN}/sendMessage", data=data
        )
