from modeltranslation.translator import translator, TranslationOptions
from .models import Works, Article, Order, Auction, AppliedArt
from django.utils.translation import gettext_lazy as _


class WorksOptions(TranslationOptions):
    fields = ['name', 'material', 'status']
    fallback_values = _('-- sorry, no translation provided --')


class AppliedArtOptions(TranslationOptions):
    fields = ['name', 'material', 'status']
    fallback_values = _('-- sorry, no translation provided --')


class ArticleOptions(TranslationOptions):
    fields = ['title', 'description', 'text']
    fallback_values = _('-- sorry, no translation provided --')


class OrderOptions(TranslationOptions):
    fields = ['status']
    fallback_values = _('-- sorry, no translation provided --')


class AuctionOptions(TranslationOptions):
    fields = ['name']


translator.register(Order, OrderOptions)
translator.register(Works, WorksOptions)
translator.register(Article, ArticleOptions)
translator.register(Auction, AuctionOptions)
translator.register(AppliedArt, AppliedArtOptions)