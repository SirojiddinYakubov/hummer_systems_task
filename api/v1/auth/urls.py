from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api.v1.auth import views

urlpatterns = [
    path("login/", views.Login.as_view()),
    path("register/", views.Register.as_view()),
    path("verify-token/", TokenRefreshView.as_view()),
    path("get-code/", views.GetCode.as_view()),
    path("verify-code/", views.VerifyCode.as_view()),
]
