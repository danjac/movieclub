from django.urls import path

from movieclub.collections import views

app_name = "collections"

urlpatterns = [
    path("", views.collection_list, name="collection_list"),
    path(
        "user/<slug:username>/",
        views.user_collection_list,
        name="user_collection_list",
    ),
    path("add/", views.add_collection, name="add_collection"),
    path(
        "<int:collection_id>/edit/",
        views.edit_collection,
        name="edit_collection",
    ),
    path(
        "<int:collection_id>/add/<int:release_id>/",
        views.add_release_to_collection,
        name="add_release_to_collection",
    ),
    path(
        "<int:collection_id>/remove/<int:release_id>/",
        views.remove_release_from_collection,
        name="remove_release_from_collection",
    ),
    path(
        "<int:collection_id>-<slug:slug>/",
        views.collection_detail,
        name="collection_detail",
    ),
]
