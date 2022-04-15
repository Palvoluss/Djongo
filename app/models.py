from ast import mod
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    quantity = models.FloatField()