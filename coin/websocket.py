"""Web Socket to watch the market data in real time"""
import cbpro
import time
import logging
from coin.coin import Coin
from coin.coinbase import currencies
from coin.analytics import Analytics


class WSClient():
    wsc = None

    def __init__(self):
        logging.debug("WSClient initializing...")

        self.wsc = CoinbaseWebsocketClient()

    def start(self, currency):
        self.currency = currency + "-USD" if currency in currencies else ""
        self.wsc.set_params(self.currency)

        self.wsc.start()
        logging.info(self.wsc.url, self.wsc.products)

    def stop(self):
        if self.wsc is not None:
            self.wsc.close()


class CoinbaseWebsocketClient(cbpro.WebsocketClient):
    def set_params(self, currency):
        self.currency = currency

        logging.debug("Setting currency to %s", self.currency)

    def on_open(self):
        self.products = [self.currency]
        self.channels = ['ticker']

        self.analytics = Analytics(self.currency)


    def on_message(self, msg):
        if 'price' in msg and 'type' in msg:
            # Example of a msg
            # {         'type': 'ticker',
            #           'sequence': 5218449005,
            #           'product_id': 'LTC-USD',
            #           'price': '47.35',
            #           'open_24h': '48.48',
            #           'volume_24h': '156948.95768504',
            #           'low_24h': '46',
            #           'high_24h': '49.36',
            #           'volume_30d': '7215772.91842438',
            #           'best_bid': '47.35',
            #           'best_ask': '47.37',
            #           'side': 'sell',
            #           'time': '2020-09-09T01:33:56.828640Z',
            #           'trade_id': 46635089,
            #           'last_size': '2.0003386'}

            crypto = Coin(self.currency)
            crypto.price = float(msg["price"])
            crypto.open = float(msg["open_24h"])
            crypto.volume = float(msg["volume_24h"])
            crypto.low = float(msg["low_24h"])
            crypto.high = float(msg["high_24h"])
            crypto.time = msg["time"]

            self.analytics.analyze(crypto)

    def on_close(self):
        print("-- Closing WebSocket --")


