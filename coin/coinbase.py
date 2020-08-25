"""Coinbase Python Client wrapper"""
import cbpro
from coin import Coin


class Coinbase:
    """Class to handle the Coinbase Python Client and to asbtract the specificities from Coin"""
    def __init__(self, currency):
        self.public_client = cbpro.PublicClient()
        self.crypto = Coin(currency)

    def get_ticker(self):
        """Get ticker from Coinbase"""
        ticker = self.public_client.get_product_ticker(product_id=self.crypto.currency)
        self.crypto.price = float(ticker["price"])
        self.crypto.volume = float(ticker["volume"])

    def get_stats(self):
        """Get Stats from Coinbase"""
        stats = self.public_client.get_product_24hr_stats(product_id=self.crypto.currency)
        self.crypto.last = float(stats["last"])
        self.crypto.low24h = float(stats["low"])
        self.crypto.high24h = float(stats["high"])
        self.crypto.open24h = float(stats["open"])

    def get_book(self):
        """Get Bids and Asks from Coinbase"""
        book = self.public_client.get_product_order_book(product_id=self.crypto.currency, level=2)
        bid_list = list()
        for bid in book["bids"]:
            order = dict()
            order["value"] = float(bid[0])
            order["size"] = float(bid[1])
            bid_list.append(order)

        ask_list = list()
        for ask in book["asks"]:
            order = dict()
            order["value"] = float(ask[0])
            order["size"] = float(ask[1])
            ask_list.append(order)

        self.crypto.money_book.calculate_ratio(bid_list, ask_list)

    def get_current(self):
        """Get the Current values of a currency"""
        self.get_ticker()
        self.get_stats()
        self.get_book()

        return self.crypto


c = Coinbase("BTC")
crypto = c.get_current()
print(crypto)
