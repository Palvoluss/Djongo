from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("deal_with_MCP/sell", views.sellBtcToMCP, name="selling_to_MCP"),
    # path("deal_with_MCP/buy", views.buyBtcFormMCP, name="buying_from_MCP"),
    path("deal_with_MCP/order", views.placeOrder, name="place_order")
    
]
