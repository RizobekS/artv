from django.utils.translation import gettext_lazy as _
from modeltranslation.translator import translator, TranslationOptions

from .models import (
    About,
    Country,
    Categories,
    Categorization,
    Dimensions,
    Seller,
    Sections,
    Services,
    Tags,
    TeamMember,
    TeamMemberExtra,
    Flow,
    Period,
    WorkType,
    Type,
    ExpertMember,
    Partner,
    AacMember,
    Aac,
    Aocv,
    AocvMember,
    AuctionRules,
    Auction
)


class TypeOptions(TranslationOptions):
    fields = ['name']
    fallback_values = _('-- sorry, no translation provided --')


class SchoolOptions(TranslationOptions):
    fields = ['name']
    fallback_values = _('-- sorry, no translation provided --')


class CountryOptions(TranslationOptions):
    fields = ["name"]
    fallback_values = _("-- sorry, no translation provided --")


class DimensionsOptions(TranslationOptions):
    fields = ["name"]
    fallback_values = _("-- sorry, no translation provided --")


class TeamMemberOptions(TranslationOptions):
    fields = ["name", "description"]
    fallback_values = _("-- sorry, no translation provided --")


class ExpertMemberOptions(TranslationOptions):
    fields = ["name", "description"]
    fallback_values = _("-- sorry, no translation provided --")


class CategoriesOptions(TranslationOptions):
    fields = ["name", "content"]
    fallback_values = _("-- sorry, no translation provided --")


class AboutOptions(TranslationOptions):
    fields = ["title", "text"]
    fallback_values = _("-- sorry, no translation provided --")


class ServicesOptions(TranslationOptions):
    fields = ['name', 'content']


class CategorizationOptions(TranslationOptions):
    fields = ['name']


class TagsOptions(TranslationOptions):
    fields = ['name']


class SectionOptions(TranslationOptions):
    fields = ['name']


class WorkTypeOption(TranslationOptions):
    fields = ['name', 'description']


class FlowOptions(TranslationOptions):
    fields = ['name']


class PeriodOptions(TranslationOptions):
    fields = ['name']


class SellerOptions(TranslationOptions):
    fields = ['name']


class PartnerOptions(TranslationOptions):
    fields = ['name', 'description']
    fallback_values = _("-- sorry, no translation provided --")


class AacMemberOptions(TranslationOptions):
    fields = ['name', 'description']
    fallback_values = _('-- sorry, no translation provided --')


class AacOptions(TranslationOptions):
    fields = ['title', 'description', 'bottom_text']
    fallback_values = _('-- sorry, no translation provided --')


class AocvOptions(TranslationOptions):
    fields = ['title', 'text']
    fallback_values = _('-- sorry, no translation provided --')


class AocvMembersOptions(TranslationOptions):
    fields = ['name', 'text']
    fallback_values = _('-- sorry, no translation provided --')


class TeamMemberExtraOptions(TranslationOptions):
    field = ['name', 'description']
    fallback_values = _("-- sorry, no translation provided --")


class AuctionRulesOptions(TranslationOptions):
    field = ['content']
    fallback_values = _("-- sorry, no translation provided --")


class AuctionOptions(TranslationOptions):
    fields = ['name', 'adress', 'content']


translator.register(About, AboutOptions)
translator.register(Country, CountryOptions)
translator.register(Categories, CategoriesOptions)
translator.register(Categorization, CategorizationOptions)
translator.register(Dimensions, DimensionsOptions)
translator.register(Seller, SellerOptions)
translator.register(Sections, SectionOptions)
translator.register(Services, ServicesOptions)
translator.register(Tags, TagsOptions)
translator.register(TeamMember, TeamMemberOptions)
translator.register(Type, TypeOptions)
translator.register(Period, PeriodOptions)
translator.register(Flow, FlowOptions)
translator.register(WorkType, WorkTypeOption)
translator.register(ExpertMember, ExpertMemberOptions)
translator.register(Partner, PartnerOptions)
translator.register(AacMember, AacMemberOptions)
translator.register(Aac, AacOptions)
translator.register(Aocv, AocvOptions)
translator.register(AocvMember, AocvMembersOptions)
translator.register(TeamMemberExtra, TeamMemberExtraOptions)
translator.register(AuctionRules, AuctionRulesOptions)
translator.register(Auction, AuctionOptions)
