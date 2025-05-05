from django.contrib import admin

from django.contrib import admin
from .models import SignupLog, LoginLog, OTP

@admin.register(SignupLog)
class SignupLogAdmin(admin.ModelAdmin):
    list_display = ("user", "users_id", "signup_time")  # Fields shown in the admin list view
 # Enable search by username and UUID
    readonly_fields = ("signup_time",)  # Prevent editing signup time

@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    list_display = ("user", "login_time")
    readonly_fields = ("login_time",)  # Make login_time read-only


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'created_at')