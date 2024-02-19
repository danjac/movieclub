from django.urls import path

from movieclub.reviews import views

app_name = "reviews"

urlpatterns = [
    path("new/<int:release_id>/", views.add_review, name="add_review"),
    path("edit/<int:review_id>/", views.edit_review, name="edit_review"),
    path("delete/<int:review_id>/", views.delete_review, name="delete_review"),
    path("<int:review_id>/", views.review_detail, name="review_detail"),
]
