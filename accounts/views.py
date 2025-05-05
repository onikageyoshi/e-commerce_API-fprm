from rest_framework import status
from django.shortcuts import render
from rest_framework import response, status, permissions, views
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import SignupSerializer, LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from .models import OTP
from .serializers import SendOTPSerializer, VerifyOTPSerializer, ResetPasswordSerializer
import random
from django.template.response import TemplateResponse 




User = get_user_model() 





class SignupView(views.APIView):
    def get(self, request):
        # Render the HTML template for signup/login
        return TemplateResponse(request, "auth.html", {})

    @swagger_auto_schema(
        request_body=SignupSerializer,
        responses={
            201: openapi.Response("Signup successful", SignupSerializer),
            400: "Bad request - Invalid data",
        },
        operation_summary="User Signup",
        operation_description="Register a new user with first name, last name, email, and password."
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Signup successful",
                "user_id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    def get(self, request):
        return TemplateResponse(request, "auth.html", {})

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response("Login successful", LoginSerializer),
            400: "Bad request - Invalid credentials",
        },
        operation_summary="User Login",
        operation_description="Authenticate user using email and password, and return access tokens."
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "user_id": user.id,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class SendOTPView(views.APIView):
    """Send an OTP to the user's email for password reset."""

    @swagger_auto_schema(
        request_body=SendOTPSerializer,
        responses={200: openapi.Response("OTP sent successfully")},
    )
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

            otp_code = random.randint(111111, 999999) 

            # Check if OTP already exists for the user
            otp_entry, created = OTP.objects.get_or_create(user=user)
            otp_entry.otp = otp_code  # Update OTP code
            otp_entry.save()

            send_mail(
                "Your OTP Code",
                f"Your OTP code is {otp_code}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return Response({"message": "OTP sent to email"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(views.APIView):
    """Verify the OTP sent to the user's email."""

    @swagger_auto_schema(
        request_body=VerifyOTPSerializer,
        responses={200: openapi.Response("OTP verified successfully")},
    )
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(views.APIView):
    """Reset the user's password after OTP verification."""

    @swagger_auto_schema(
        request_body=ResetPasswordSerializer,
        responses={200: openapi.Response("Password reset successful")},
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)