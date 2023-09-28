from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import (
    AppliedArt,
    AppliedArtPriceUp,
    Article,
    Auctions,
    Cart,
    CartItem,
    Discounts,
    Gallery,
    Likes,
    Order,
    ProductReview,
    Views,
    WorkPriceUp,
    Works,
    SizeArts,
)


class WorkPriceUpAdmin(admin.ModelAdmin):
    pass


class AppliedArtPriceUpAdmin(admin.ModelAdmin):
    pass


class WorkPriceUpInline(admin.StackedInline):
    model = WorkPriceUp


class AppliedArtPriceUpInline(admin.StackedInline):
    model = AppliedArtPriceUp


@admin.action(description='Поставить статус "Продано"')
def make_sold(modeladmin, request, querset):
    querset.update(status='sold')


class WorksAdmin(TranslationAdmin, admin.ModelAdmin):
    list_display = ["name", "author", "uid_name", "status_ru", "pub_date"]
    search_fields = ('name', 'author__name', 'u_id',)
    inlines = (WorkPriceUpInline,)
    fields = ('u_id', 'section', 'name', 'views', 'photo', 'add_watermark', 'author', 'owner_number_contract', 'type',
              'genre', 'sizes', 'dimensions', 'year_of_creation', 'price', 'period', 'flow', 'show_in_service',
              'signature',
              'description', 'age_restriction', 'country', 'regions', 'quantity', 'discount', 'shoppable', 'popular',
              'material', 'tags', 'price_up', 'seller', 'for_interier', 'status', 'starts_at', 'ends_at', 'slug')
    actions = [make_sold]


class ArticleAdmin(TranslationAdmin):
    list_display = ["id", "title"]


class AppliedArtAdmin(TranslationAdmin, admin.ModelAdmin):
    list_display = ["name", "author", "uid_name", "status_ru", "pub_date"]
    search_fields = ('name', 'author__name', 'u_id',)
    inlines = (AppliedArtPriceUpInline,)
    fields = ('u_id', 'vid', 'type', 'school', 'photo', 'add_watermark', 'name', 'views', 'author', 'year_of_creation', 'period',
              'description', 'material', 'size',  'dimensions', 'price', 'tags', 'country',
              'regions', 'price_up', 'seller', 'for_interier', 'age_restriction', 'quantity',
              'discount', 'status', 'starts_at', 'ends_at', 'shoppable', 'popular')
    actions = [make_sold]


class CartAdmin(admin.ModelAdmin):
    pass


class SizeArtsAdmin(admin.ModelAdmin):
    list_display = ["name"]
    fields = ("name", "height", "width")


class CartItemAdmin(admin.ModelAdmin):
    pass


class OrderAdmin(admin.ModelAdmin):
    pass


class LikesAdmin(admin.ModelAdmin):
    pass


class DiscountsAdmin(admin.ModelAdmin):
    pass


class ProductReviewAdmin(admin.ModelAdmin):
    pass


class AuctionAdmin(TranslationAdmin):
    pass


class GalleryAdmin(admin.ModelAdmin):
    pass


class ViewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Cart, CartAdmin)
admin.site.register(Views, ViewAdmin)
admin.site.register(Works, WorksAdmin)
admin.site.register(SizeArts, SizeArtsAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Likes, LikesAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Auctions, AuctionAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Discounts, DiscountsAdmin)
admin.site.register(AppliedArt, AppliedArtAdmin)
admin.site.register(WorkPriceUp, WorkPriceUpAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(AppliedArtPriceUp, AppliedArtPriceUpAdmin)