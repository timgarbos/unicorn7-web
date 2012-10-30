from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    avatar = models.TextField()
    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })