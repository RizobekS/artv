from django.utils.translation import gettext_lazy as _
from modeltranslation.translator import translator, TranslationOptions

from .models import Authors, SecondAuthor, Socials, Craftmanship


class AuthorOptions(TranslationOptions):
    fields = ['name', 'occupation', 'bio']
    fallback_values = _('-- sorry, no translation provided --')


class SecondAuthorOptions(TranslationOptions):
    fields = ['name', 'occupation', 'bio']
    fallback_values = _('-- sorry, no translation provided --')


class SocialOptions(TranslationOptions):
    fields = ['name']
    fallback_values = _('-- sorry, no translation provided --')


class CraftmanshipOptions(TranslationOptions):
    fields = ['name']


translator.register(Authors, AuthorOptions)
translator.register(SecondAuthor, SecondAuthorOptions)
translator.register(Socials, SocialOptions)
translator.register(Craftmanship, CraftmanshipOptions)
