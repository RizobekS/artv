from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import AuthUsers, Authors, Socials, Craftmanship, SecondAuthor


class AuthUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('phone', 'email', 'first_name', 'last_name', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('phone', 'email', 'first_name', 'last_name')
    search_fields = ('phone',)
    ordering = ('first_name',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('last_login',)


class AuthorAdmin(TranslationAdmin):
    pass


class SecondAuthorAdmin(TranslationAdmin):
    pass


class SocialsAdmin(TranslationAdmin):
    pass


class CraftsmanshipAdmin(TranslationAdmin):
    pass


admin.site.register(Authors, AuthorAdmin)
admin.site.register(SecondAuthor, SecondAuthorAdmin)
admin.site.register(Socials, SocialsAdmin)
admin.site.register(AuthUsers, AuthUserAdmin)
admin.site.register(Craftmanship, CraftsmanshipAdmin)
