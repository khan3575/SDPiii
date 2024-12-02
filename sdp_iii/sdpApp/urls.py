from django.urls import path,include
from . import views
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')

urlpatterns =  [
   path('', views.redirect_home, name='redirect'),
   path('signup/',views.signup, name='signup'),
   path('home/',views.home, name='home'),
   path('login/',views.login_view, name= 'login'),
   path('following/',views.following, name='following'),
   path('write_blog/', views.write_blog, name= 'write_blog'),
   path('profile/', views.profile_show, name='profile'),
   path('profile/edit/', views.edit_profile, name='edit_profile'),
   path('about/', views.about, name='about'),
   path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
   path('logout/', logout_view, name='logout'),
   path('blog/<int:blog_id>/', views.show_blog, name='show_blog'),
   
]