from django import forms
from .models import Order


class OrderCreationForm(forms.ModelForm):
    def clean_price(self):
        token_price = self.cleaned_data["token_price"]
        if token_price < 0:
            raise forms.ValidationError("Price can not be negative")
        return token_price

    def clean_token_quantity(self):
        token_qty = self.cleaned_data["token_qty"]
        if token_qty < 0:
            raise forms.ValidationError("BTC quantity can not be negative")
        return token_qty

    class Meta:
        model = Order
        fields = ("token_price", "token_qty")

class SellForm(forms.ModelForm):
    def clean_token_quantity(self):
        token_qty = self.cleaned_data["token_qty"]
        if token_qty < 0:
            raise forms.ValidationError("BTC quantity can not be negative")
        return token_qty

    class Meta:
        model = Order
        fields = ["token_qty"]