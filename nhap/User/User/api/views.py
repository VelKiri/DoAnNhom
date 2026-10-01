from django.shortcuts import redirect
from django.contrib.auth import login

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer, LoginSerializer


# =========================
# REGISTER API
# =========================

class RegisterAPIView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return redirect("login")

        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


# =========================
# LOGIN API
# =========================

class LoginAPIView(APIView):

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.validated_data["user"]

            login(request, user)

            return redirect("home")

        # Đăng nhập sai
        from django.contrib import messages

        messages.error(
            request,
            "Mật khẩu hoặc email không đúng! Vui lòng nhập lại."
        )

        return redirect("login")