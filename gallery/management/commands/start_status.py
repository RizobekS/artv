from django.core.management.base import BaseCommand
from gallery.status_check import main


class Command(BaseCommand):
    def handle(self, *args, **options):
        main()