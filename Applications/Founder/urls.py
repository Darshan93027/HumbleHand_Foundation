from django.urls import path
from . import views
from Applications.humblehand.views import common_login_view

urlpatterns = [
    path('login/',common_login_view, name='Founder_login'),
    path('signup/', views.signup, name='Founder_signup'),
    path('logout/', views.logout_view, name='Founder_logout'),
    path('user-data/', views.user_data, name='Founder_user_data'),
    path('volunteers/', views.volunteer_data, name='Founder_volunteer_data'),
    path('messages/', views.message_data, name='Founder_message_data'),
    path('dashboard/', views.Dashboard, name='Founder_dashboard'),
    path('donations/', views.donation_data, name='Founder_donation_data'),
    path('messages/delete/', views.delete_message, name='delete_message'),
    path('messages/send-reply/', views.send_reply, name='send_reply'),

]
