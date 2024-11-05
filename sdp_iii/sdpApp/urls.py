from django.urls import path,include
from .views import *


urlpatterns =  [
    path("accounts/",include("django.contrib.auth.urls")),
    path("signup/",authView, name="authView"),
    path("", home, name="home"),
]