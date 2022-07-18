import random

from django.shortcuts import get_object_or_404

from app.models import Wallet


def generate_random_number(max_value):
    return random.uniform(1, max_value)

def get_user_balance(user):
    balance = {
        'token': Wallet.objects.filter(user=user).first().token_balance,
        'fiat': Wallet.objects.filter(user=user).first().fiat_balance,
    }

    return balance 

def can_action(action, user_wallet, user_balance, token_qty, price):
    if action == "sell":
        if user_wallet.token_balance < token_qty:
            return False
        return True
    else:
        if user_balance < token_qty * price:
            return False
        return True

def return_num(a):
    return float(a)

