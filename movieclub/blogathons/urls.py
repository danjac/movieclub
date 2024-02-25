from django.urls import path

from movieclub.blogathons import views

app_name = "blogathons"

urlpatterns = [
    path("", views.blogathon_list, name="blogathon_list"),
]
