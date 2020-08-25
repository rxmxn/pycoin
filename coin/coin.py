import numpy

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


class Coin:
    """Coin is the main object that represents a cryto-currency"""
    def __init__(self, currency):
        self.currency = currency + "-USD" if currency in currencies else ""
        self.price = 0
        self.low24h = 0
        self.high24h = 0
        self.last = 0
        self.open24h = 0
        self.volume = 0
        self.money_book = MoneyBook()

    def __str__(self):
        coin_string = list()
        coin_string.append("Currency: %s" % (self.currency))
        coin_string.append("Current Price: %s" % (str(self.price)))
        coin_string.append("Last: %s" % (str(self.last)))
        coin_string.append("Volume: %s" % (str(self.volume)))
        coin_string.append("Low Today: %s" % (str(self.low24h)))
        coin_string.append("High Today: %s" % (str(self.high24h)))
        coin_string.append("Open Today: %s" % (str(self.open24h)))

        if self.money_book.trending:
            coin_string.append("Trending to Buy Ratio: %s" % (str(self.money_book.ratio)))
        else:
            coin_string.append("Trending to Sell Ratio: %s" % (str(self.money_book.ratio)))

        coin_string.append("Price VS Open: %s %%" % (str(self.percent_open())))
        coin_string.append("Price VS Last: %s %%" % (str(self.percent_last())))

        return "\n".join(coin_string)

    def percentage_difference(self, value):
        """Use to calculate different percentages compared with the current price"""
        return (self.price - value) * 100 / value

    def percent_open(self):
        """
        Calculate the percentage comparing Current Price with Open,
        which is similar to compare it with the value from 24 hours ago
        """
        return self.percentage_difference(self.open24h)

    def percent_last(self):
        """Calculate the percentage comparing Current Price with Last"""
        return self.percentage_difference(self.last)


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


