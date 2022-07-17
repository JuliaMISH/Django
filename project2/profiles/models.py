from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):  # Profile is instance
    user      = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='following', blank=True)  # here blank=True is for being able
    # to create profile instance without following anything because following is not a necessary attribute for profile
    bio       = models.TextField(default='no bio...')
    updated   = models.DateTimeField(auto_now=True)
    created   = models.DateTimeField(auto_now_add=True)

    def profiles_posts(self): #  returns all the profile's posts
        return self.post_set.all()

    def __str__(self):
        return str(self.user.username)

    class Meta:
        ordering = ('-created',)
