from django.contrib import admin
from app.models import Order, Transaction, Wallet

admin.site.register(Order)
admin.site.register(Wallet)
admin.site.register(Transaction)
