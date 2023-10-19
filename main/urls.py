from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_auth, name='home'),
    path('home_not_auth', views.home_not_auth, name="home_not_auth"),
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
]
