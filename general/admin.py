from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import (
	About,
	Country,
	Categories,
	Categorization,
	Dimensions,
	School,
	Sell,
	Seller,
	Services,
	PublishHouseArt,
	PublishHouseWork,
	Sections,
	ServicesImage,
	Tags,
	Type,
	TeamMember,
	TeamMemberExtra,
	Flow,
	Period,
	Region,
	WorkType,
	ExpertMember,
	Partner,
	Aac,
	AacMember,
	Aocv,
	AocvMember,
	AuctionRules,
	Auction,
	Lots
)


class RegionAdmin(admin.TabularInline):
	model = Region


class CountryAdmin(admin.ModelAdmin):
	inlines = [RegionAdmin]
	extra = 0


class SellRequestAdmin(admin.ModelAdmin):
	pass


class CategoriesAdmin(TranslationAdmin):
	pass


class AboutAdmin(TranslationAdmin):
	pass


class CategorizationAdmin(TranslationAdmin):
	list_display = ['name', 'section', 'order']


class TeamMemberAdmin(TranslationAdmin):
	pass


class TagsAdmin(TranslationAdmin):
	pass


class SectionAdmin(TranslationAdmin):
	pass


class SchoolAdmin(admin.ModelAdmin):
	pass


class WorkTypeAdmin(TranslationAdmin):
	pass


class TypeAdmin(TranslationAdmin):
	pass


class PeriodAdmin(TranslationAdmin):
	pass


class FlowAdmin(TranslationAdmin):
	pass


class SelleAdmin(TranslationAdmin):
	pass


class ExpertAdmin(TranslationAdmin):
	pass


class PartnerAdmin(TranslationAdmin):
	pass


class AacAdmin(TranslationAdmin):
	pass


class AacMemberAdmin(TranslationAdmin):
	pass


class AocvAdmin(TranslationAdmin):
	pass


class AocvMembersAdmin(TranslationAdmin):
	pass


class ServicesImageAdmin(admin.StackedInline):
	model = ServicesImage


class PublishHouseArtAdmin(TranslationAdmin):
	list_display = ['title', 'description', 'images']


class PublishHouseWorkAdmin(TranslationAdmin):
	list_display = ['description', 'images']


class TeamMembersExtraAdmin(TranslationAdmin):
	pass


class AuctionRulesAdmin(TranslationAdmin):
	pass


class AuctionAdmin(TranslationAdmin):
	pass


class LotsAdmin(TranslationAdmin):
	pass


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
	inlines = [ServicesImageAdmin]

	class Meta:
		model = Services


@admin.register(ServicesImage)
class ServicesImageAdmin(admin.ModelAdmin):
	pass


admin.site.register(About, AboutAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Categorization, CategorizationAdmin)
admin.site.register(Dimensions)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Seller, SelleAdmin)
admin.site.register(Sell, SellRequestAdmin)
admin.site.register(Sections, SectionAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(Flow, FlowAdmin)
admin.site.register(WorkType, WorkTypeAdmin)
admin.site.register(ExpertMember, ExpertAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Aac, AacAdmin)
admin.site.register(AacMember, AacMemberAdmin)
admin.site.register(Aocv, AocvAdmin)
admin.site.register(AocvMember, AocvMembersAdmin)
admin.site.register(TeamMemberExtra, TeamMembersExtraAdmin)
admin.site.register(AuctionRules, AuctionRulesAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Lots, LotsAdmin)
admin.site.register(PublishHouseArt, PublishHouseArtAdmin)
admin.site.register(PublishHouseWork, PublishHouseWorkAdmin)
