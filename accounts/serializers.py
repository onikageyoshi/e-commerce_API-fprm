from rest_framework import serializers
from .models import LoginLog, SignupLog
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import OTP

class SignupSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)  
    last_name = serializers.CharField(required=True)   

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']  

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        first_name = validated_data.get("first_name")  
        last_name = validated_data.get("last_name")  

        user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)  
        SignupLog.objects.create(user=user, first_name=first_name, last_name=last_name)   

        return user







class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):  
        email = attrs.get("email")  
        password = attrs.get("password")  

        if not email or not password:
            raise serializers.ValidationError({"non_field_errors": ["Both email and password are required."]})

        user = authenticate(username=email, password=password)  
        if user is None:
            raise serializers.ValidationError({"non_field_errors": ["Invalid Email or Password."]})

        attrs["user"] = user  
        return attrs  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginLog
        fields = '__all__'


class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get("email")
        otp_code = data.get("otp")

        try:
            user = User.objects.get(email=email)
            otp = OTP.objects.filter(user=user, code=otp_code).last()

            if not otp or not otp.is_valid():
                raise serializers.ValidationError("Invalid or expired OTP.")
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        return data


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def validate(self, data):
        email = data.get("email")
        new_password = data.get("new_password")
        user = User.objects.get(email=email)

        if user.check_password(new_password):
            raise serializers.ValidationError("New password cannot be the same as the old password.")

        return data

    def save(self):
        email = self.validated_data["email"]
        new_password = self.validated_data["new_password"]
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()


        