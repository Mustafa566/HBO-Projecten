
from django.db import models
from django.contrib.auth.models import AbstractUser
from .CustomUserManager import CustomUserManager

class CustomUser(AbstractUser):
    objects = CustomUserManager()
    
    role = models.TextField(blank=True)

    def __str__(self):
        return self.username