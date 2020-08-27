"""Base Crypto class that will be used in the system"""
import numpy


def percentage_difference(price, value):
    """Use to calculate different percentages compared with the current price"""
    return (price - value) * 100 / value if value != 0 else 0


class Coin:
    """Coin is the main object that represents a cryto-currency"""
    def __init__(self, currency):
        self.currency = currency
        self.price = 0
        self.low = 0
        self.high = 0
        self.last = 0
        self.open = 0
        self.close = 0
        self.volume = 0
        self.time = ""
        self.money_book = MoneyBook()

    def __str__(self):
        coin_string = list()
        coin_string.append("Currency: %s" % (self.currency))
        if self.price != 0:
            coin_string.append("Current Price: %s" % (str(self.price)))
        if self.close != 0:
            coin_string.append("Closed Price: %s" % (str(self.close)))
        if self.last != 0:
            coin_string.append("Last: %s" % (str(self.last)))
        if self.volume != 0:
            coin_string.append("Volume: %s" % (str(self.volume)))
        if self.low != 0:
            coin_string.append("Low: %s" % (str(self.low)))
        if self.high != 0:
            coin_string.append("High: %s" % (str(self.high)))
        if self.open != 0:
            coin_string.append("Open: %s" % (str(self.open)))
        if self.money_book.bids != 0 and self.money_book.asks != 0:
            coin_string.append("Bids: %s" % (str(self.money_book.bids)))
            coin_string.append("Asks: %s" % (str(self.money_book.asks)))
            action = "Buy" if self.money_book.trending else "Sell"
            coin_string.append("Trending to %s Ratio: %s" % (action, str(self.money_book.ratio)))

        coin_string.append("Time: %s" % self.time)

        if self.price != 0:
            coin_string.append("Price VS Open: %s %%" % (str(self.percent_open())))
            coin_string.append("Price VS Last: %s %%" % (str(self.percent_last())))

        return "\n".join(coin_string)

    def percent_open(self):
        """
        Calculate the percentage comparing Current Price with Open,
        which is similar to compare it with the value from 24 hours ago
        """
        return percentage_difference(self.price, self.open)

    def percent_last(self):
        """Calculate the percentage comparing Current Price with Last"""
        return percentage_difference(self.price, self.last)


class MoneyBook:
    """Represents bids/asks and estimate ratio"""
    def __init__(self):
        self.ratio = 0
        # trending = True means that people are buyng more than selling
        self.trending = False
        self.bids = 0
        self.asks = 0
        self.orders = list()

    def calculate_ratio(self, bid_list, ask_list):
        """
        Get the ratio in which asks(people buying)/bids(people selling) is currently at
        This might help perceiving a trend at a certain time
        """
        result_bids = list()
        for bid in bid_list:
            result_bids.append(bid["value"] * bid["size"])
        self.bids = numpy.mean(result_bids)

        result_asks = list()
        for ask in ask_list:
            result_asks.append(ask["value"] * ask["size"])
        self.asks = numpy.mean(result_asks)

        if self.bids > self.asks:
            self.trending = True
            self.ratio = self.bids/self.asks - 1
        else:
            self.trending = False
            self.ratio = self.asks/self.bids - 1
