from django.urls import path,include
from . import views
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')

urlpatterns =  [
   path('', views.redirect_home, name='redirect'),
   path('myblogs/', views.myblogs, name='myblogs'),
   path('blog/<int:blog_id>/', views.blog_details, name='blog_details'),
   path('signup/',views.signup, name='signup'),
   path('home/',views.home, name='home'),
   path('login/',views.login_view, name= 'login'),
   path('following/',views.following, name='following'),
   path('follow_user/<int:user_id>/', views.follow_user, name='follow_user'),  # Follow/Unfollow path
   path('write_blog/', views.write_blog, name= 'write_blog'),
   path('profile/show/', views.profile_show, name='profile_show'),
   path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
   path('profile/edit/', views.edit_profile, name='edit_profile'),
   path('about/', views.about, name='about'),
   path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
   path('logout/', logout_view, name='logout'),
   
   
]