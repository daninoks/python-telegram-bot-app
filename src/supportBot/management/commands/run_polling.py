from django.core.management.base import BaseCommand
from supportBot.dispatcher import run_pooling


class Command(BaseCommand):
    """
    `python manage.py run_polling`
    Before start make sure WebHook deleted:
    https://api.telegram.org/bot{TOKEN}/deleteWebhook?url=https://domain.ltd/

    And afterwards set WebHook back:
    https://api.telegram.org/bot{TOKEN}/setWebhook?url=https://domain.ltd/
    """

    help = 'Polling mode for supportBot app'

    def handle(self, *args, **options):
        run_pooling()
