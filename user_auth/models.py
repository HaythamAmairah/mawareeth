from django.db import models
from django.contrib.auth.models import User

User._meta.get_field('email').blank = False

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Profile'
