from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField(
        "self", blank=True, symmetrical=False, related_name="follow")

    def __str__(self):
        return f"{self.username}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.CharField(max_length=350)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name="likepost")
    unlikes = models.ManyToManyField(
        User, blank=True, related_name="unlikepost")

    def likes_counter(self):
        return self.likes.all().count() - self.unlikes.all().count()

    def __str__(self):
        return f"{self.user} {self.post} {self.created}"
