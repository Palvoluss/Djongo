import random

from django.shortcuts import get_object_or_404
from django.core.exceptions import SuspiciousOperation
from django import forms

from app.models import Wallet


def generate_random_number(max_value):
    return random.uniform(1, max_value)

def get_user_balance(user):
    balance = {
        'token': Wallet.objects.filter(user=user).first().token_balance,
        'fiat': Wallet.objects.filter(user=user).first().fiat_balance,
    }

    return balance 

def can_action(action, user_wallet, user_balance, token_qty, pric, token_price):
    validation = {
        'can': False,
        'message': ''
    }

    if action == "sell":
        if token_qty < 0:
            validation['can'] = False
            validation['message'] = 'You can\'t sell negative amount'
            return validation

        if user_wallet.token_balance < token_qty:
            validation['can'] = False
            validation['message'] = 'You can\'t sell more token than you have in your wallet'
            return validation

        validation['can'] = True
        validation['message'] = 'Here\'s your fiat..'
        return validation
    
    elif action == "buy":
        if  token_price < 0:
            validation['can'] = False
            validation['message'] = 'You can\'t buy negative amount'
            return validation

        if user_wallet.fiat_balance < token_price:
            validation['can'] = False
            validation['message'] = 'You can\'t buy if you don\'t have enough fiat'
            return validation

        validation['can'] = True
        validation['message'] = 'Glad you came on the dark side, we have Bitcoin'
        return validation




