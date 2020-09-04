"""Web Socket to watch the market data in real time"""
import cbpro
import time
import logging
from coin.coin import Coin
from coin.coinbase import Coinbase, currencies


class myWebsocketClient(cbpro.WebsocketClient):
    def set_currency(self, currency):
        self.currency = currency + "-USD" if currency in currencies else ""
        logging.debug("Setting currency to %s", self.currency)

    def on_open(self):
        self.products = [self.currency]
        self.message_count = 0
        self.channels = ['ticker']

    def on_message(self, msg):
        self.message_count += 1
        if 'price' in msg and 'type' in msg:
            print ("Message type:", msg["product_id"],
                   "\t@ {:.3f}".format(float(msg["price"])))

    def on_close(self):
        print("-- Closing WebSocket --")


