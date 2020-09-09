"""Web Socket to watch the market data in real time"""
import cbpro
import time
import logging
from coin.coin import Coin
from coin.coinbase import Coinbase, currencies
from pymongo import MongoClient


class WSClient():
    wsc = None

    def __init__(self):
        logging.debug("WSClient initializing...")

        self.wsc = CoinbaseWebsocketClient()

        mongo_client = MongoClient('mongodb://localhost:27017/')
        # specify the database
        db = mongo_client.cryptocurrency_database
        self.collection = db.crypto_collection


    def start(self, currency):
        self.currency = currency + "-USD" if currency in currencies else ""
        self.wsc.set_params(self.currency, self.collection)

        self.wsc.start()
        logging.info(self.wsc.url, self.wsc.products)

    def stop(self):
        if self.wsc is not None:
            self.wsc.close()


class CoinbaseWebsocketClient(cbpro.WebsocketClient):
    def set_params(self, currency, collection):
        self.currency = currency
        self.collection = collection

        logging.debug("Setting currency to %s", self.currency)

    def on_open(self):
        self.products = [self.currency]
        self.channels = ['ticker']
        self.mongo_collection=self.collection


    def on_message(self, msg):
        if 'price' in msg and 'type' in msg:
            print(msg)
            self.collection.insert_one({"currency": msg["product_id"], "price": msg["price"]})
            # I can create an analytics class that this function can call
            # to analyze the message. In that class I can have functions
            # that will make the choices, including STOP_LOSS.
            # I can create a coin object with the msg and then pass that coin
            # to the analytics class or function.

    def on_close(self):
        print("-- Closing WebSocket --")


