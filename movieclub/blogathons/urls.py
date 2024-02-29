from django.urls import path

from movieclub.blogathons import views

app_name = "blogathons"

urlpatterns = [
    path("", views.blogathon_list, name="blogathon_list"),
    path("add/", views.add_blogathon, name="add_blogathon"),
    path(
        "<int:blogathon_id>/edit/",
        views.edit_blogathon,
        name="edit_blogathon",
    ),
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
        "<int:blogathon_id>/proposals/submit/",
        views.submit_proposal,
        name="submit_proposal",
    ),
    path(
        "<int:proposal_id>/proposals/respond/",
        views.respond_to_proposal,
        name="respond_to_proposal",
    ),
    path(
        "<int:blogathon_id>/entries/submit/",
        views.submit_entry,
        name="submit_entry",
    ),
    path(
        "<slug:slug>-<int:blogathon_id>/",
        views.blogathon_detail,
        name="blogathon_detail",
    ),
]
