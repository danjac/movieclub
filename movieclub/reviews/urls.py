from django.urls import path

from movieclub.reviews import views

app_name = "reviews"

urlpatterns = [
    path("<int:release_id>/new/", views.add_review, name="add_review"),
    path("<int:review_id>/edit/", views.edit_review, name="edit_review"),
    path("<int:review_id>/cancel/", views.cancel_review, name="cancel_review"),
    path("<int:review_id>/delete/", views.delete_review, name="delete_review"),
    path("<int:parent_id>/reply/", views.reply_to_review, name="reply_to_review"),
]
