from django.urls import path

from movieclub.people import views

app_name = "people"

urlpatterns = [
    path("actors/<slug:slug>-<int:person_id>/", views.cast_member, name="cast_member"),
    path("crew/<slug:slug>-<int:person_id>/", views.crew_member, name="crew_member"),
]
