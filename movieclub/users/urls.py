from django.urls import path

from movieclub.users import views

app_name = "users"

urlpatterns = [
    path("edit/", views.edit_user_details, name="edit_user_details"),
    path("<slug:username>/profile/", views.user_detail, name="user_detail"),
]
