# #!/usr/bin/env python
# # This program is dedicated to the public domain under the CC0 license.
# # pylint: disable=import-error,wrong-import-position
# """
# Simple example of a bot that uses a custom webhook setup and handles custom updates.
# For the custom webhook setup, the libraries `starlette` and `uvicorn` are used. Please install
# them as `pip install starlette~=0.20.0 uvicorn~=0.17.0`.
# Note that any other `asyncio` based web server framework can be used for a custom webhook setup
# just as well.
# Usage:
# Set bot token, url, admin chat_id and port at the start of the `main` function.
# You may also need to change the `listen` value in the uvicorn configuration to match your setup.
# Press Ctrl-C on the command line or send a signal to the process to stop the bot.
# """
# import time
#
# import asyncio
# import html
# import logging
# from dataclasses import dataclass
# from http import HTTPStatus
#
# import uvicorn
# from starlette.applications import Starlette
# from starlette.requests import Request
# from starlette.responses import PlainTextResponse, Response
# from starlette.routing import Route
#
# import json
# import requests
# # from django.http import (
# #     JsonResponse,
# #     HttpResponse,
# #     HttpRequest,
# # )
#
# from django.conf import settings
# from django.db.transaction import atomic, non_atomic_requests
# from django.http import HttpResponse, HttpResponseForbidden
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_POST
#
# from django.http import JsonResponse
# from django.shortcuts import render
# from django.views import View
# from django.core.management.base import BaseCommand
# from django.conf import settings
# # from testApp.views import TutorialBotView
# # from telegram.request import HttpRequest
# from asgiref.sync import sync_to_async
# from asgiref.sync import async_to_sync
#
#
# import os
# from dotenv import load_dotenv
# from pathlib import Path
#
# from telegram import __version__ as TG_VER
#
# try:
#     from telegram import __version_info__
# except ImportError:
#     __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]
#
# if __version_info__ < (20, 0, 0, "alpha", 1):
#     raise RuntimeError(
#         f"This example is not compatible with your current PTB version {TG_VER}. To view the "
#         f"{TG_VER} version of this example, "
#         f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
#     )
#
# from telegram import Update
# from telegram.constants import ParseMode
# from telegram.ext import (
#     Application,
#     CallbackContext,
#     CommandHandler,
#     ContextTypes,
#     ExtBot,
#     TypeHandler,
# )
#
# dotenv_path = Path('../../django_project/.env')
# load_dotenv(dotenv_path=dotenv_path)
#
#
# API_TOKEN = os.getenv('TOKEN')
# # API_TOKEN = '5497164468:AAEhn_kbJz-y0UDgWghSzlj8ktNsjmOUf3A'
# print(API_TOKEN)
#
#
# # Enable logging
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )
# logger = logging.getLogger(__name__)
#
#
# @dataclass
# class WebhookUpdate:
#     """Simple dataclass to wrap a custom update type"""
#
#     user_id: int
#     payload: str
#
#
# class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):
#     """
#     Custom CallbackContext class that makes `user_data` available for updates of type
#     `WebhookUpdate`.
#     """
#
#     @classmethod
#     def from_update(
#         cls,
#         update: object,
#         application: "Application",
#     ) -> "CustomContext":
#         if isinstance(update, WebhookUpdate):
#             return cls(application=application, user_id=update.user_id)
#         return super().from_update(update, application)
#
#
# async def start(update: Update, context: CustomContext) -> None:
#     """Display a message with instructions on how to use this bot."""
#     url = context.bot_data["url"]
#     payload_url = html.escape(f"{url}/submitpayload?user_id=<your user id>&payload=<payload>")
#     text = (
#         f"To check if the bot is still running, call <code>{url}/healthcheck</code>.\n\n"
#         f"To post a custom update, call <code>{payload_url}</code>."
#     )
#     await update.message.reply_html(text=text)
#
#
# async def webhook_update(update: WebhookUpdate, context: CustomContext) -> None:
#     """Callback that handles the custom updates."""
#     chat_member = await context.bot.get_chat_member(chat_id=update.user_id, user_id=update.user_id)
#     payloads = context.user_data.setdefault("payloads", [])
#     payloads.append(update.payload)
#     combined_payloads = "</code>\n??? <code>".join(payloads)
#     text = (
#         f"The user {chat_member.user.mention_html()} has sent a new payload. "
#         f"So far they have sent the following payloads: \n\n??? <code>{combined_payloads}</code>"
#     )
#     await context.bot.send_message(
#         chat_id=context.bot_data["admin_chat_id"], text=text, parse_mode=ParseMode.HTML
#     )
#     print('in webhook_update')
#
#
# def send_message(message, chat_id):
#         TELEGRAM_URL = "https://api.telegram.org/bot"
#         API_TOKEN = '5497164468:AAEhn_kbJz-y0UDgWghSzlj8ktNsjmOUf3A'
#         data = {
#             "chat_id": chat_id,
#             "text": message,
#             "parse_mode": "Markdown",
#         }
#         response = requests.post(
#             f"{TELEGRAM_URL}{API_TOKEN}/sendMessage", data=data
#         )
#
#
# # requests.post('https://194-67-74-48.cloudvps.regruhosting.ru/webhook/')
# @csrf_exempt
# @async_to_sync
# async def telegram(request) -> JsonResponse:
#         """Handle incoming Telegram updates by putting them into the `update_queue`"""
#         await main()
#         await application.update_queue.put(
#             Update.de_json(data=await request.json(), bot=application.bot)
#         )
#
#         t_data = json.loads(request.body)
#         t_data = request.json()
#         send_message(msg, t_id)
#
#         return JsonResponse({"ok": "POST request processed"})
#
#
# # class TelegramView(View):
# #     def get(self, request, *args, **kwargs):
# #         return JsonResponse({"ok": "GET request processed"})
# #
# #     def post(self, request, *args, **kwargs):
# #         t_data = json.loads(request.body)
# #         # print(t_data)
# #
# #
# #         url = 'https://194-67-74-48.cloudvps.regruhosting.ru/webhook/'
# #         admin_chat_id = '3206063'
# #         port = 8000
# #
# #         context_types = ContextTypes(context=CustomContext)
# #
# #         # # Here we set updater to None because we want our custom webhook server to handle the updates
# #         # # and hence we don't need an Updater instance
# #         # application = (
# #         #     Application.builder().token(API_TOKEN).updater(None).context_types(context_types).build()
# #         # )
# #         #
# #         # # save the values in `bot_data` such that we may easily access them in the callbacks
# #         # application.bot_data["url"] = url
# #         # application.bot_data["admin_chat_id"] = admin_chat_id
# #         #
# #         # # register handlers
# #         # application.add_handler(CommandHandler("app", start))
# #         # application.add_handler(TypeHandler(type=WebhookUpdate, callback=webhook_update))
# #         #
# #         #
# #         # application.update_queue.put(
# #         #     Update.de_json(data=json.loads(request.body), bot=application.bot)
# #         # )
# #         # application.start()
# #         # application.stop()
# #         # # print('in telegram def')
# #
# #         t_id = t_data["message"]["chat"]["id"]
# #         msg = "worked"
# #         self.send_message(msg, t_id)
# #
# #         return JsonResponse({"ok": "POST request processed"})
# #
# #     @staticmethod
# #     def send_message(message, chat_id):
# #         TELEGRAM_URL = "https://api.telegram.org/bot"
# #         API_TOKEN = '5497164468:AAEhn_kbJz-y0UDgWghSzlj8ktNsjmOUf3A'
# #         data = {
# #             "chat_id": chat_id,
# #             "text": message,
# #             "parse_mode": "Markdown",
# #         }
# #         response = requests.post(
# #             f"{TELEGRAM_URL}{API_TOKEN}/sendMessage", data=data
# #         )
#
#
# # # Set up webserver
# # async def telegram(request: HttpRequest) -> HttpResponse:
# #     """Handle incoming Telegram updates by putting them into the `update_queue`"""
# #     await application.update_queue.put(
# #         Update.de_json(data=await HttpRequest.json(), bot=application.bot)
# #     )
# #     print('in telegram def')
# #
# #     t_data = json.loads(HttpRequest.body)
# #     data = {
# #         "chat_id": admin_chat_id,
# #         "text": 'WTF IS IT WORKING?',
# #         "parse_mode": "Markdown",
# #     }
# #     response = requests.post(
# #         f"{TELEGRAM_URL}{TUTORIAL_BOT_TOKEN}/sendMessage", data=data
# #     )
# #     return HttpResponse({"ok": "POST request processed"})
#
#
# async def main() -> None:
#     """Set up the application and a custom webserver."""
#     url = 'https://194-67-74-48.cloudvps.regruhosting.ru/webhook/'
#     admin_chat_id = 3206063
#     port = 8000
#
#     context_types = ContextTypes(context=CustomContext)
#
#     # Here we set updater to None because we want our custom webhook server to handle the updates
#     # and hence we don't need an Updater instance
#     application = (
#         Application.builder().token(API_TOKEN).updater(None).context_types(context_types).build()
#     )
#
#     # save the values in `bot_data` such that we may easily access them in the callbacks
#     application.bot_data["url"] = url
#     application.bot_data["admin_chat_id"] = admin_chat_id
#
#     # register handlers
#     application.add_handler(CommandHandler("app", start))
#     application.add_handler(TypeHandler(type=WebhookUpdate, callback=webhook_update))
#
#
#     # # Set up webserver
#     # @csrf_exempt
#     # @async_to_sync
#     # async def telegram(request) -> JsonResponse:
#     #         """Handle incoming Telegram updates by putting them into the `update_queue`"""
#     #         await application.update_queue.put(
#     #             Update.de_json(data=await request.json(), bot=application.bot)
#     #         )
#     #
#     #         # t_data = json.loads(request.body)
#     #         # t_data = request.json()
#     #         # send_message(msg, t_id)
#     #
#     #         return JsonResponse({"ok": "POST request processed"})
#
#
#     # async def telegram(request: Request) -> Response:
#     #     """Handle incoming Telegram updates by putting them into the `update_queue`"""
#     #     await application.update_queue.put(
#     #         Update.de_json(data=await request.json(), bot=application.bot)
#     #     )
#     #     return Response()
#
#     # async def custom_updates(request: Request) -> PlainTextResponse:
#     #     """
#     #     Handle incoming webhook updates by also putting them into the `update_queue` if
#     #     the required parameters were passed correctly.
#     #     """
#     #     try:
#     #         user_id = int(request.query_params["user_id"])
#     #         payload = request.query_params["payload"]
#     #     except KeyError:
#     #         return PlainTextResponse(
#     #             status_code=HTTPStatus.BAD_REQUEST,
#     #             content="Please pass both `user_id` and `payload` as query parameters.",
#     #         )
#     #     except ValueError:
#     #         return PlainTextResponse(
#     #             status_code=HTTPStatus.BAD_REQUEST,
#     #             content="The `user_id` must be a string!",
#     #         )
#     #
#     #     await application.update_queue.put(WebhookUpdate(user_id=user_id, payload=payload))
#     #     return PlainTextResponse("Thank you for the submission! It's being forwarded.")
#
#     # async def health(_: Request) -> PlainTextResponse:
#     #     """For the health endpoint, reply with a simple plain text message."""
#     #     return PlainTextResponse(content="The bot is still running fine :)")
#     #
#     # starlette_app = Starlette(
#     #     routes=[
#     #         Route("/telegram", telegram, methods=["POST"]),
#     #         Route("/healthcheck", health, methods=["GET"]),
#     #         Route("/submitpayload", custom_updates, methods=["POST", "GET"]),
#     #     ]
#     # )
#     # webserver = uvicorn.Server(
#     #     config=uvicorn.Config(
#     #         app=starlette_app,
#     #         port=port,
#     #         use_colors=False,
#     #         host="127.0.0.1",
#     #     )
#     # )
#
#     # Run application and webserver together
#     async with application:
#         await application.start()
#         await asyncio.sleep(100)
#         # await webserver.serve()
#         await application.stop()
#
#
#     # Run application and webserver together
#     # async with application:
#     #     try:
#     #         await application.start()
#     #         time.sleep(1000)
#     #         await application.stop()
#     #     # await webserver.serve()
#     #     except KeyboardInterrupt:
#     #         print("Program terminated manually!")
#     #         await application.stop()
#     #         raise SystemExit
#
#
# # if __name__ == "__main__":
# #     asyncio.run(main())
#
# class Command(BaseCommand):
#     help = 'HELP here'
#
#     def handle(self, *args, **options):
#         print('in handle')
#         asyncio.run(main())
