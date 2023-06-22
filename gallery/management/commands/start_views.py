from django.core.management.base import BaseCommand
from gallery.views_import import main


class Command(BaseCommand):
    def handle(self, *args, **options):
        main()