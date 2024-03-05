from django.urls import path

from movieclub.reviews import views

app_name = "reviews"

urlpatterns = [
    path("release/<int:release_id>/", views.add_review, name="release_review_list"),
    path("release/<int:release_id>/new/", views.add_review, name="add_review"),
    path("user/<slug:username>/", views.add_review, name="release_user_list"),
    path("<int:review_id>/", views.review_detail, name="review_detail"),
    path("<int:review_id>/edit/", views.edit_review, name="edit_review"),
    path("<int:review_id>/delete/", views.delete_review, name="delete_review"),
]
