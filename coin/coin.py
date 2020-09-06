"""Base Crypto class that will be used in the system"""
import numpy
import json
from flask import Flask, jsonify


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
        self.market_cap = 0
        self.money_book = MoneyBook()
        self.rating = Rating()

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
        if self.market_cap != 0:
            coin_string.append("Market Capital: %s" % (str(self.market_cap)))
        if self.money_book.bids != 0 and self.money_book.asks != 0:
            coin_string.append("Bids: %s" % (str(self.money_book.bids)))
            coin_string.append("Asks: %s" % (str(self.money_book.asks)))
            action = "Buy" if self.money_book.trending else "Sell"
            coin_string.append("Trending to %s Ratio: %s" % (action, str(self.money_book.ratio)))

        if len(self.time) > 0:
            coin_string.append("Time: %s" % self.time)

        if self.price != 0:
            coin_string.append("Price VS Open: %s %%" % (str(self.percent_open())))
            coin_string.append("Price VS Last: %s %%" % (str(self.percent_last())))

        coin_string.append(str(self.rating))

        return "\n".join(coin_string)

    def to_json(self):
        data = {}
        data["Currency"] = self.currency

        if self.price != 0:
            data["Price"] = self.price
            data["Price_VS_Open_%"] = self.percent_open()

        if self.close != 0:
            data["Close"] = self.close

        if self.last != 0:
            data["Last"] = self.last

        if self.volume != 0:
            data["volume"] = self.volume

        if self.low != 0 or self.high != 0:
            data["Low"] = self.low
            data["High"] = self.high

        if self.open != 0:
            data["Open"] = self.open

        if self.market_cap != 0:
            data["Market_Capital"] = self.market_cap

        if len(self.time) > 0:
            data["Time"] = self.time

        if len(self.rating.fcas_rating) > 0:
            data["Rating"] = self.rating.to_json()

        if self.money_book.bids != 0 and self.money_book.asks != 0:
            data["MoneyBook"] = self.money_book.to_json()

        return jsonify(data)

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

    def to_json(self):
        data = {}
        data["Bids"] = self.bids
        data["Asks"] = self.asks
        data["Trending"] = "UP" if self.trending else "DOWN"
        data["TrendingRatio"] = self.ratio
        return data

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


class Rating:
    """Shows a current rating of the crypto currency"""
    def __init__(self):
        self.fcas_rating = ""
        self.fcas_score = 0
        self.developer_score = 0
        self.market_maturity_score = 0
        self.utility_score = 0
        self.last_refreshed = ""

    def __str__(self):
        coin_string = list()

        if len(self.fcas_rating) > 0:
            coin_string.append("FCAS Rating: %s" % self.fcas_rating)
            coin_string.append("FCAS Score: %s" % str(self.fcas_score))
            coin_string.append("Developer Score: %s" % str(self.developer_score))
            coin_string.append("Market Maturity Score: %s" % str(self.market_maturity_score))
            coin_string.append("Utility Score: %s" % str(self.utility_score))
            coin_string.append("Last Refreshed: %s" % self.last_refreshed)

            return ", ".join(coin_string)
        else:
            return ""

    def to_json(self):
        data = {}
        data["FCAS_Rating"] = self.fcas_rating
        data["FCAS_Score"] = self.fcas_score
        data["Developer_Score"] = self.developer_score
        data["Market_Maturity_Score"] = self.market_maturity_score
        data["Utility_Score"] = self.utility_score
        data["Last_Refreshed"] = self.last_refreshed
        return data

