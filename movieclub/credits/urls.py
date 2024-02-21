from django.urls import path

from movieclub.credits import views

app_name = "credits"

urlpatterns = [
    path("cast/", views.cast_list, name="cast_list"),
    path(
        "cast/<slug:slug>-<int:person_id>/",
        views.cast_detail,
        name="cast_detail",
    ),
    path("crew/", views.crew_list, name="crew_list"),
    path(
        "crew/<slug:slug>-<int:person_id>/",
        views.crew_detail,
        name="crew_detail",
    ),
]
