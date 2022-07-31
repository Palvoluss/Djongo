from django.contrib import messages
from django.forms import ValidationError
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from app.cmc_price import CMC_Info_About
from app.forms import BuyForm, OrderCreationForm, SellForm
from app.models import Order, Wallet
from app.utils import can_action, get_user_balance


def home(request):
    if request.user.is_authenticated:
        balance = get_user_balance(request.user)
        sell_available = balance['token'] is not None and balance['token'] > 0
        buy_availabile = balance['fiat'] is not None and balance['fiat'] > 0
        return render(request, 'home/home_layout.html', {
            'tokens_price': CMC_Info_About().get_BTC_ETH_XRP_dict(), 
            'balance': balance,
            'can_buy': buy_availabile,
            'can_sell': sell_available
            })
    else:
        return render(request, 'home/home_layout.html', {
        'tokens_price': CMC_Info_About().get_BTC_ETH_XRP_dict()}
        )

@login_required
def sellBtcToMCP(request):
    balance = get_user_balance(request.user)
    action = request.path.split('/').pop()
    form = SellForm()
    cmc_info = CMC_Info_About()

    if request.method == "POST":
        form = SellForm(request.POST)
        if form.is_valid():
            user_wallet = Wallet.objects.filter(user=request.user).first()
            btc_quantity = form.cleaned_data["token_qty"]

            validation = can_action(action, user_wallet, balance, btc_quantity, cmc_info.get_btc_data())

            if not validation['can']:
                print(validation['message'])
                return redirect("home")

            
            order = form.save()
            order.user = request.user
            order.type = "sell"
            order.order_status = "pending"
            order.save()

            user_wallet.token_balance -= btc_quantity
            user_wallet.fiat_balance += btc_quantity * cmc_info.get_btc_data()
            user_wallet.save()

            print(validation['message'])
            messages.success(request, "You sell your BTC to MCP, MCP praise you")

            return redirect("home")

    context = {
        "form": form,
        "orders": Order.objects.filter(user=request.user),
        "balance": get_user_balance(request.user),
        'tokens_price': CMC_Info_About().get_BTC_ETH_XRP_dict(),
    }

    return render(request, "home/orders/sell_to_mcp.html", context)

@login_required
def placeOrder(request):
    user_balance = get_user_balance(request.user)
    action = request.path.split('/').pop()
    form = OrderCreationForm()

    if request.method == "POST":
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            user_wallet = Wallet.objects.filter(user=request.user).first()
            btc_quantity = form.cleaned_data["token_qty"]
            price = form.cleaned_data["token_price"]

            if not can_action(action, user_wallet, user_balance, btc_quantity, price):
                if action == "order":
                    messages.error(request, "You do not have enough BTC to sell ")
                else:
                    messages.error(request, "You do not have enough money to buy BTC")
                return redirect("home")

            order = form.save()
            order.user = request.user
            order.order_status = "pending"
            order.save()

            user_wallet.btc_balance -= btc_quantity
            user_wallet.save()

            messages.success(request, "Your sell order has been placed!")

            return redirect("home")

    context = {
        "form": form,
        "orders": Order.objects.filter(user=request.user),
        "balance": get_user_balance(request.user),
        'tokens_price': CMC_Info_About().get_BTC_ETH_XRP_dict(),
    }

    return render(request, "home/orders/sell_buy.html", context)

@login_required
def buyBtcFormMCP(request):
    balance = get_user_balance(request.user)
    action = request.path.split('/').pop()
    form = BuyForm()
    cmc_info = CMC_Info_About()

    if request.method == "POST":
        form = BuyForm(request.POST)
        if form.is_valid():
            user_wallet = Wallet.objects.filter(user=request.user).first()
            token_price = form.cleaned_data["token_price"]

            validation = can_action(action, user_wallet, balance, None, cmc_info.get_btc_data(), token_price)

            if not validation['can']:
                print(validation['message'])
                return redirect("home")

            
            order = form.save()
            order.user = request.user
            order.type = "buy"
            order.order_status = "pending"
            order.save()

            user_wallet.fiat_balance -= token_price
            user_wallet.token_balance += token_price / cmc_info.get_btc_data()
            user_wallet.save()

            print(validation['message'])
            messages.success(request, "You sell your BTC to MCP, MCP praise you")

            return redirect("home")

    context = {
        "form": form,
        "orders": Order.objects.filter(user=request.user),
        "balance": get_user_balance(request.user),
        'tokens_price': CMC_Info_About().get_BTC_ETH_XRP_dict(),
    }

    return render(request, "home/orders/sell_to_mcp.html", context)

@login_required
def sellBTCForm(rrequest):
    return