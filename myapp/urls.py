from django.urls import path, include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('', views.home, name='home'), 
    path('home/', views.home, name='home'),                      # Home page
    path('navbar/', views.navbar, name='navbar'), 
    path('search/', views.Search, name='search'),           

    path('signup/', views.Signup, name='signup'),           # Signup page
    path('login/', views.Login, name='login'),              # Login page
    path('logout/', views.Logout, name='logout'),           # Logout view

    path('profile/', views.user_profile, name='profile'),   # View user profile
    path('update_profile/', views.UpdateProfile, name='update_profile'),  # Update profile

    path('donate/', views.Donate, name='donate'),
    path('volunteer/', views.volunteer_view, name='volunteer'),
    path('payment_success/', views.payment_success, name='payment_success'),

    path('receipt/<str:order_id>/', views.donation_receipt_view, name='donation_receipt'),

    path('donation_history/', views.donation_history_view, name='donation_history'),
    path('message_history/', views.message_history_view, name='message_history'),
    path('contact/',views.contact_view, name='contact'),

    path('download-apk/', views.download_apk, name='download_apk'),
    

    path('water_conservation/',views.water_conservation, name='water_conservation'),
    path('pedh_lagao/',views.pedh_lagao, name='pedh_lagao'),
    path('green_campus/',views.green_campus, name='green_campus'),
    path('tree_plantation/',views.tree_plantation, name='tree_plantation'),
    path('water_event/',views.water_event, name='water_event'),
    path('excellence_award/',views.excellence_award, name='excellence_award'),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
