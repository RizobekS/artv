from django.core.management.base import BaseCommand
from gallery.tgbot.main import main


class Command(BaseCommand):
    def handle(self, *args, **options):
        main()

