from django.urls import path

from movieclub.collections import views

app_name = "collections"

urlpatterns = [
    path("", views.collection_list, name="collection_list"),
    path("add/", views.add_collection, name="add_collection"),
    path("<int:collection_id>/edit/", name="collection_edit"),
    path(
        "<int:collection_id>/add/<int:release_id>/",
        name="add_resource_to_collection",
    ),
    path(
        "<int:collection_id>/remove/<int:release_id>/",
        name="remove_resource_from_collection",
    ),
    path("<int:collection_id>-<slug:slug>/", name="collection_detail"),
]
