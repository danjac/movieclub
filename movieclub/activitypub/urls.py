from django.urls import path

from movieclub.activitypub import views

app_name = "activitypub"

urlpatterns = [
    path(".wellknown/webfinger/", views.webfinger, name="webfinger"),
    path("nodeinfo/2.0/", views.nodeinfo, name="nodeinfo"),
    path("user/<slug:username>/", views.local_user, name="local_user"),
]
