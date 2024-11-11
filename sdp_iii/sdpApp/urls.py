from django.urls import path,include
from . import views

urlpatterns =  [
   path('signup/',views.signup, name='signup'),
   path('home/',views.home, name='home'),
   path('login/',views.login_view, name= 'login'),
   
]