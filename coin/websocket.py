"""Web Socket to watch the market data in real time"""
import cbpro
import time
import logging
import threading
from coin.coin import Coin
from coin.coinbase import Coinbase, currencies

# TODO: Check why do I need threading. Is it really doing anything now?
# How can I take advantage of threading?
# Do I really need this class at all if I will not use Threading?
class WSClient(threading.Thread):
    wsc = None

    def __init__(self):
        logging.debug("WSClient initializing...")

        self.wsc = CoinbaseWebsocketClient()

        threading.Thread.__init__(self)

    def start(self, currency):
        self.currency = currency + "-USD" if currency in currencies else ""
        self.wsc.set_currency(self.currency)

        self.wsc.start()
        logging.info(self.wsc.url, self.wsc.products)

    def stop(self):
        if self.wsc is not None:
            self.wsc.close()


class CoinbaseWebsocketClient(cbpro.WebsocketClient):
    def set_currency(self, currency):
        self.currency = currency
        logging.debug("Setting currency to %s", self.currency)

    def on_open(self):
        self.products = [self.currency]
        self.channels = ['ticker']

    def on_message(self, msg):
        if 'price' in msg and 'type' in msg:
            print(msg["price"])
            # I can create an analytics class that this function can call
            # to analyze the message. In that class I can have functions
            # that will make the choices, including STOP_LOSS.
            # I can create a coin object with the msg and then pass that coin
            # to the analytics class or function.

    def on_close(self):
        print("-- Closing WebSocket --")


