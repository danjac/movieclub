from django.urls import path

from movieclub.credits import views

app_name = "credits"

urlpatterns = [
    path("actors/", views.cast_members, name="cast_members"),
    path("actors/<slug:slug>-<int:person_id>/", views.cast_member, name="cast_member"),
    path("crew/", views.crew_members, name="crew_members"),
    path("crew/<slug:slug>-<int:person_id>/", views.crew_member, name="crew_member"),
]
