from django.urls import path
from django.contrib import admin

from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('panel/', views.panel, name='panel'),
    path('login/', views.login, name='login'),
    path('logout/', views.mylogout, name='logout'),
    path('register/', views.register, name='register'),
    path('tables/', views.tables, name='tables'),
    path('charts/', views.charts, name='charts'),
    path('panel/site_setting', views.site_setting, name='site_setting'),
    path('panel/change', views.change_pass, name='change_pass'),
    path('panel/error', views.error, name='error'),
    path('panel/profile', views.profile, name='profile'),
    path('profile/delete-person/<int:pk>/', views.delete_person, name='delete-person'),
    path('profile/edit-person/<int:pk>/', views.edit_person, name='edit-person'),
    path('user/', views.user_page, name='user'),
]
