from django.core.management.base import BaseCommand
from gallery.watermarker import main


class Command(BaseCommand):
    def handle(self, *args, **options):
        main()
