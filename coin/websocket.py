"""Web Socket to watch the market data in real time"""
import cbpro
import time
from coin.coin import Coin
from coin.coinbase import Coinbase, currencies


class myWebsocketClient(cbpro.WebsocketClient):
    def initialize(self):
        self.currencies = list()

    def add_currency(self, currency):
        currency = currency + "-USD" if currency in currencies else ""
        self.currencies.append(currency)

    def on_open(self):
        self.products = self.currencies
        self.message_count = 0
        self.channels = ['ticker']

    def on_message(self, msg):
        self.message_count += 1
        if 'price' in msg and 'type' in msg:
            print ("Message type:", msg["type"],
                   "\t@ {:.3f}".format(float(msg["price"])))

    def on_close(self):
        print("-- Closing WebSocket --")


