from django.urls import path

from movieclub.blogathons import views

app_name = "blogathons"

urlpatterns = [
    path("", views.blogathon_list, name="blogathon_list"),
    path("add/", views.add_blogathon, name="add_blogathon"),
    path(
        "<int:blogathon_id>/publish/",
        views.publish_blogathon,
        name="publish_blogathon",
    ),
    path(
        "<int:blogathon_id>/proposals/",
        views.blogathon_proposals,
        name="blogathon_proposals",
    ),
    path(
        "<slug:slug>-<int:blogathon_id>/",
        views.blogathon_detail,
        name="blogathon_detail",
    ),
]
