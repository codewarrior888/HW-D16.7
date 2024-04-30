from django.urls import path

from .views import EmailVerification, home, signup_view, login_view, logout_view, successful_verification, verification_failed


urlpatterns = [
    path('signup', signup_view, name='signup'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('email_verification/<int:pk>', EmailVerification.as_view(), name='email_verification'),
    path('successful_verification', successful_verification, name='successful_verification'),
    path('verification_failed', verification_failed, name='verification_failed'),
    path('', home, name='home'),
]
