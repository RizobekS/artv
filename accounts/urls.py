from .views import *
from django.urls import path


app_name = "accounts"
urlpatterns = [
    path('register/', register, name="register"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
]
