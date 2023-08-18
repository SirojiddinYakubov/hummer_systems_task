from django.urls import path

from api.v1.users import views

urlpatterns = [
    path("list/", views.UsersList.as_view()),
    path("me/", views.UsersMe.as_view()),
    path("set-password/", views.SetPassword.as_view()),
]
