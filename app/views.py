from django.shortcuts import render
from django.http import HttpResponse

from app.cmc_price import CMC_Info_About


def home(request):
    token_price = CMC_Info_About().get_data()
    return render(request, 'home/home_layout.html', {'token_price': token_price})