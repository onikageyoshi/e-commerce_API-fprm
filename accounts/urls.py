from django.urls import path
from .views import SignupView, LoginView, SendOTPView, VerifyOTPView, ResetPasswordView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('login/', LoginView.as_view(), name='login-user'),
    path("signup/", SignupView.as_view(), name="signup-user"),
]
