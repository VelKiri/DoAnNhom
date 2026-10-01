from django.urls import path
from .views import RegisterAPIView, LoginAPIView


urlpatterns = [

    path(
        "register/",
        RegisterAPIView.as_view(),
        name="api_register"
    ),

    path(
        "login/",
        LoginAPIView.as_view(),
        name="api_login"
    ),
]