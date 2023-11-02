from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    # UserLoginCreateView, 
    # UserRegistrationCreateView,
    # logout_view,
    # ClientRegistrationCreateView,
    show_notification,
    delete_notification,
    profile_view,
    ProfileUpdateView,
    TimezoneUpdateView
)

app_name = 'authentication'

urlpatterns = [
    # path('login', UserLoginCreateView.as_view(), name='login'),
    # path('logout/', logout_view, name='logout'),
    # path('signup/', UserRegistrationCreateView.as_view(), name='sign_up'),
    # path('signup_client/', ClientRegistrationCreateView.as_view(), name='cient_sign_up'),
    path('notification/<int:notification_id>/',show_notification,name='show_notifications'),
    path('notification/delete/<int:notification_id>/',delete_notification,name='delete_notification'),
    path('profile/',profile_view,name='profile'),
    path('<pk>/update', ProfileUpdateView.as_view(), name='profile-update'),
    path('<pk>/timezone/update', TimezoneUpdateView.as_view(), name='timezone-update'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="account/password_reset.html"),name="reset_password"), 
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),name="password_reset_done"),

]
