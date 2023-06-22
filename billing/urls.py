from django.urls import path

from . import views


app_name = "billing"
urlpatterns = [
    path('payme/', views.payme_view, name='payme-create'),
    path('apelsin/', views.apelsin_view, name='apelsin-create'),
    path('payme-redirect/', views.payme_redirect_page, name="payme_redirect"),
    path('apelsin-redirect/', views.apelsin_redirect_page, name="apelsin_redirect")
]
