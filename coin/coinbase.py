"""Coinbase Python Client wrapper"""
import time
from datetime import datetime
import cbpro
from coin.coin import Coin

currencies = [
        "ALGO", "DASH", "OXT", "ATOM", "KNC",
        "XRP", "REP", "MKR", "OMG", "COMP",
        "BAND", "XLM", "EOS", "ZRX", "BAT",
        "LOOM", "CVC", "DNT", "MANA", "GNT",
        "LINK", "BTC", "LTC", "ETH", "BCH",
        "ETC", "ZEC", "XTZ", "DAI"]

granularity = {
        "1minute":60,
        "5minutes":300,
        "15minutes":900,
        "1hour":3600,
        "6hours":21600,
        "1day":86400
        }

class Coinbase:
    """Class to handle the Coinbase Python Client and to asbtract the specificities from Coin"""
    def __init__(self, currency):
        self.public_client = cbpro.PublicClient()
        self.currency = currency + "-USD" if currency in currencies else ""

    def __get_ticker(self, crypto):
        """Get ticker from Coinbase and update the crypto reference"""
        ticker = self.public_client.get_product_ticker(product_id=self.currency)
        crypto.price = float(ticker["price"])
        crypto.volume = float(ticker["volume"])
        crypto.time = ticker["time"]

    def __get_stats(self, crypto):
        """Get Stats from Coinbase and update the crypto reference"""
        stats = self.public_client.get_product_24hr_stats(product_id=self.currency)
        crypto.last = float(stats["last"])
        crypto.low = float(stats["low"])
        crypto.high = float(stats["high"])
        crypto.open = float(stats["open"])

    def __get_book(self, crypto):
        """Get Bids and Asks from Coinbase and update the crypto reference"""
        book = self.public_client.get_product_order_book(product_id=self.currency, level=2)
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

        crypto.money_book.calculate_ratio(bid_list, ask_list)

    def get_current(self):
        """Get the Current values of a currency"""
        crypto = Coin(self.currency)

        self.__get_ticker(crypto)
        self.__get_stats(crypto)
        self.__get_book(crypto)

        return crypto

    def get_historic_rates(self, start=None, end=None, gran="1day", n_elements=1):
        """Retrieve n-elements from historic data from start date to end date"""

        # Since this function is accessing historic data
        # and there is a limit of 1 call/second to this endpoint as a public member,
        # adding a 1 second delay each time this function is called
        time.sleep(1)

        historic = self.public_client.get_product_historic_rates(
                product_id=self.currency, start=start, end=end, granularity=granularity[gran]
                )

        coin_list = list()

        if len(historic["message"]) > 0:
            print(historic["message"])
            return coin_list

        for hist in historic:
            hist_crypto = Coin(self.currency)
            hist_crypto.time = datetime.utcfromtimestamp(hist[0]).strftime('%Y-%m-%d %H:%M:%S')
            hist_crypto.low = hist[1]
            hist_crypto.high = hist[2]
            hist_crypto.open = hist[3]
            hist_crypto.close = hist[4]
            hist_crypto.volume = hist[5]
            coin_list.append(hist_crypto)

        return coin_list[:n_elements]
