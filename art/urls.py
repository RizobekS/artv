from django.urls import path
from django.contrib import admin
from django.conf.urls.static import static
from django.urls.conf import include, re_path
from django.conf.urls.i18n import i18n_patterns

from art import settings
from general.views import Home
from .views import set_language_from_url, robots

admin.site.site_header = 'Art Vernissage'
admin.site.site_title = 'ArtV'

urlpatterns = [
                  path("set_language/<str:user_language>/",
                       set_language_from_url, name="set_language_from_url"),
                  path('admin/', admin.site.urls),
                  path('i18n/', include('django.conf.urls.i18n')),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('robots.txt', robots)
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    re_path('^$', Home.as_view(), name='home_page'),
    re_path(r'', include('general.urls')),
    path('accounts/', include("accounts.urls")),
    path('gallery/', include("gallery.urls")),
    path('billing/', include("billing.urls")),
)

admin.site.site_header = 'Администрирование ART VERNISSAGE'
# handler404 = "general.views.error_404_view"
