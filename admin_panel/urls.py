from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('admin_user/', views.admin_user, name='admin_user'),
    path('admin_donation/', views.admin_donation, name='admin_donation'),
    path('admin_messages/', views.admin_messages, name='admin_messages'),
    path('admin_mobile_app/', views.admin_mobile_app, name='admin_mobile_app'),
    path('admin_volunteer/', views.admin_volunteer, name='admin_volunteer'),
    path('sample/', views.sample, name='sample'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),

]