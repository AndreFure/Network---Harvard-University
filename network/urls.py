
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-post", views.create_post, name="create-post"),
    path("profile/<str:username>", views.user_profile, name="profile"),
    path("post/<int:post_id>", views.post_likes, name="post_likes"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post")
]
