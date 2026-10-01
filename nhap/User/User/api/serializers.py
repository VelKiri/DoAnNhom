from rest_framework import serializers
from nhap.User.User.models import CustomUser
from django.contrib.auth import authenticate


# =========================
# REGISTER
# =========================

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "password2"]

    def validate(self, data):

        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                "Mật khẩu nhập lại không khớp!"
            )

        if CustomUser.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError(
                "Email đã được sử dụng!"
            )

        if CustomUser.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError(
                "Tên đăng nhập đã tồn tại!"
            )

        return data

    def create(self, validated_data):

        validated_data.pop("password2")

        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        return user


# =========================
# LOGIN
# =========================

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        email = data["email"]
        password = data["password"]

        user = authenticate(
            username=email,
            password=password
        )

        if user is None:
            raise serializers.ValidationError(
                "Email hoặc mật khẩu không đúng!"
            )

        data["user"] = user

        return data