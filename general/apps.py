from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GeneralConfig(AppConfig):
    name = 'general'
    verbose_name = _('Главный')
