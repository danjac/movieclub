from django.urls import path

from movieclub.blogathons import views

app_name = "blogathons"

urlpatterns = [
    path("", views.blogathon_list, name="blogathon_list"),
    path(
        "user/<slug:username>/",
        views.blogathons_for_user,
        name="blogathons_for_user",
    ),
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
        "proposals/<int:proposal_id>/",
        views.proposal_detail,
        name="proposal_detail",
    ),
    path(
        "proposals/<int:proposal_id>/respond/",
        views.respond_to_proposal,
        name="respond_to_proposal",
    ),
    path(
        "<int:blogathon_id>/entries/submit/",
        views.submit_entry,
        name="submit_entry",
    ),
    path(
        "entries/<int:entry_id>/",
        views.entry_detail,
        name="entry_detail",
    ),
    path(
        "entries/<int:entry_id>/edit/",
        views.edit_entry,
        name="edit_entry",
    ),
    path(
        "entries/<int:entry_id>/delete/",
        views.delete_entry,
        name="delete_entry",
    ),
    path(
        "<slug:slug>-<int:blogathon_id>/",
        views.blogathon_detail,
        name="blogathon_detail",
    ),
]
