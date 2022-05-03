from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from app.cmc_price import CMC_Info_About
from app.forms import OrderCreationForm
from app.models import Wallet
from app.utils import get_user_balance


def home(request):
    tokens_price = {
        'BTC': CMC_Info_About().get_btc_data(),
        'ETH': CMC_Info_About().get_eth_data(),
        'XRP': CMC_Info_About().get_xrp_data(),
    }
    if request.user.is_authenticated:
        balance = get_user_balance(request.user)
        sell_available = balance['token'] is not None and balance['token'] > 0
        buy_availabile = balance['fiat'] is not None and balance['fiat'] > 0
        print(buy_availabile, sell_available)
        return render(request, 'home/home_layout.html', {
            'tokens_price': tokens_price, 
            'balance': balance,
            'can_buy': buy_availabile,
            'can_sell': sell_available }
            )
    else:
        return render(request, 'home/home_layout.html', {
        'tokens_price': tokens_price}
        )

@login_required
def sellOrBuyFormMCP(request):
    form = OrderCreationForm()
    if request.method == "POST":
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            user_wallet = Wallet.objects.filter(user=request.user).first()
            btc_quantity = form.cleaned_data["btc_quantity"]

            if not canSell(user_wallet, btc_quantity):
                messages.error(request, "You do not have enouth BTC to sell ")
                return redirect("home")

            order = form.save()
            order.user = request.user
            order.type = "sell"
            order.order_status = "pending"
            order.save()

            user_wallet.btc_balance -= btc_quantity
            user_wallet.save()

            messages.success(request, "Your sell order has been placed!")
            match_sell_order(order)

            return redirect("home")

    context = {
        "form": form,
        "orders": Order.objects.filter(user=request.user),
        "balance": getUserBalance(request.user),
    }

    return render(request, "mainApp/order.html", context) 


