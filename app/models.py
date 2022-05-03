from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from djongo.models.fields import ObjectIdField

class Wallet(models.Model):
    _id = ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token_balance = models.FloatField()
    fiat_balance = models.FloatField()

    def save(self, *args, **kwargs):
        super(Wallet, self).save(*args, **kwargs)
        
class Order(models.Model):
    _id = ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(choices=(("buy", "buy"), ("sell", "sell")), max_length=20)
    order_status = models.CharField(choices=(("pending", "pending"),("failed", "failed"), ("completed", "completed")), max_length=20)
    token_price = models.FloatField()
    token_qty = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Transaction(models.Model):
    _id = ObjectIdField()
    buyer = models.ForeignKey(User, related_name="buyer", on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name="seller", on_delete=models.CASCADE)
    token_pice = models.FloatField()
    token_qty = models.FloatField()
    datetime = models.DateTimeField(auto_now_add=True)
