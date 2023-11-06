from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Recipes(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    cuisine = models.CharField(max_length=64)
    time = models.PositiveIntegerField()
    ingredients = models.JSONField()
    steps = models.JSONField()
    calories = models.PositiveIntegerField()
    image = models.URLField(max_length=255, blank=True)
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name="recipes")
    likes = models.PositiveIntegerField(default=0)
    
class Favourites(models.Model):
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name="favourites")
    title = models.ForeignKey('Recipes', on_delete=models.CASCADE, related_name="favourites")