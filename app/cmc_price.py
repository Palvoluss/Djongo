import os
import requests

from dotenv import load_dotenv

load_dotenv()


class CMC_Info_About:

    def __init__(self):
        # API Parameters
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.params = {
            'start': '1',
            'limit': '10',
            'convert': 'USD'
        }
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': str(os.getenv('CMC_APIKEY'))
        }

    def get_btc_data(self):
        # Gathering data
        r = requests.get(url=self.url, headers=self.headers, params=self.params).json()
        price = round(list(filter(lambda crypto: crypto['symbol'] == 'BTC', r['data']))[0]['quote']['USD']['price'], 8)
        return price

    def get_eth_data(self):
        # Gathering data
        r = requests.get(url=self.url, headers=self.headers, params=self.params).json()
        price = round(list(filter(lambda crypto: crypto['symbol'] == 'ETH', r['data']))[0]['quote']['USD']['price'],8)
        return price
    
    def get_xrp_data(self):
        # Gathering data
        r = requests.get(url=self.url, headers=self.headers, params=self.params).json()
        price = round(list(filter(lambda crypto: crypto['symbol'] == 'XRP', r['data']))[0]['quote']['USD']['price'], 8)
        return price


