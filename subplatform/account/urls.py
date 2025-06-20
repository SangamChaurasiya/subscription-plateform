from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name=""),
    path('register', views.register, name="register"),
    path('my-login', views.my_login, name="my-login"),
    path('user-logout', views.user_logout, name="user-logout"),

    # Password Management

    # 1 - Allow us to enter our email in order to receive a password reset link
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="account/password-reset.html"), name='password_reset'),
    
    # 2 - Show a success message stating that an email was sent to reset our password
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="account/password-reset-sent.html"), name='password_reset_done'),
    
    # 3 - Send a link to our email, so that we can reset our password + We will be prompted to enter in a new password
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="account/password-reset-form.html"), name='password_reset_confirm'),
    
    # 4 - Show a success message stating that our password was changed
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="account/password-reset-complete.html"), name='password_reset_complete'),

    # Email Verification
    path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name='email-verification'),
    path('email-verification-sent', views.email_verification_sent, name='email-verification-sent'),
    path('email-verification-success', views.email_verification_success, name='email-verification-success'),
    path('email-verification-failed', views.email_verification_failed, name='email-verification-failed'),
]
