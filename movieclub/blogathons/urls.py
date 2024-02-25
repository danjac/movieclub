from django.urls import path

from movieclub.blogathons import views

app_name = "blogathons"

urlpatterns = [
    path("", views.blogathon_list, name="blogathon_list"),
    path("add/", views.add_blogathon, name="add_blogathon"),
    path(
        "<slug:slug>/<int:blogathon_id>/",
        views.blogathon_detail,
        name="blogathon_detail",
    ),
]
