from django.urls import path
from blog import views

app_name = "blog"  # URL Reverse

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/", views.post_detail, name="post_detail"),
    path("<int:post_pk>/comments/", views.comment_list, name="comment_list"),
    path("<int:post_pk>/comments/new/", views.comment_new, name="comment_new"),
    path("<int:post_pk>/comments/<int:pk>/edit/", views.comment_edit, name="comment_edit"),
    path("<int:post_pk>/comments/<int:pk>/delete/", views.comment_delete, name="comment_delete"),
]
