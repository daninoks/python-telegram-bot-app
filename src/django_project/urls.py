"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.decorators.csrf import csrf_exempt

# from rest_framework import routers
from testApp.views import TelegramBotWebhookView
# from testApp.management.commands.hardcode import TelegramView
# from testApp.management.commands.hardcode import telegram



# router = routers.SimpleRouter()
# path('webhook/', csrf_exempt(TutorialBotView.as_view())),
# path('webhook/', csrf_exempt(hardcode.telegram))

urlpatterns = [
    path('webhook/', csrf_exempt(TelegramBotWebhookView.as_view())),
    path('admin/', admin.site.urls),
]
