from django.db import models
from django.contrib.auth.models import AbstractUser


class ChessAnalyticsUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(blank=True, max_length=30)
    last_name = models.CharField(blank=True, max_length=30)
    rating = models.IntegerField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(blank=True, max_length=30)
    piece_preference = models.CharField(default='cburnett')
    notation_preference = models.CharField(default='uci')
