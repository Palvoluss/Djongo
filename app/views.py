from django.shortcuts import render
from django.http import HttpResponse

from app.cmc_price import CMC_Info_About
from app.models import Wallet
from app.utils import get_user_balance


def home(request):
    tokens_price = {
        'BTC': CMC_Info_About().get_btc_data(),
        'ETH': CMC_Info_About().get_eth_data(),
        'XRP': CMC_Info_About().get_xrp_data(),
    }
    
    balance = get_user_balance(request.user)
    return render(request, 'home/home_layout.html', {
        'tokens_price': tokens_price, 
        'balance': balance}
        )
