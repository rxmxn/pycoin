"""Analytics class to run the logic to do transactions"""
import time
import logging
from datetime import datetime, date, timedelta
from coin.coin import Coin
from coin.alphavantage import AlphaVantage


class Analytics:
    def __init__(self, currency):
        self.currency = currency
        self.lower_limit = 0
        self.acceptable_percentage = 2
        self.acceptable_score_difference = 20
        self.acceptable_open_percentage_difference = 2
        self.sell_flag = False
        self.buy_flag = False

    def set_acceptable_percentage(self, acceptable_percentage):
        self.acceptable_percentage = acceptable_percentage

    def set_acceptable_score_difference(self, acceptable_score_difference):
        self.acceptable_score_difference = acceptable_score_difference

    def set_acceptable_open_percentage_difference(self, acceptable_open_percentage_difference):
        self.acceptable_open_percentage_difference = acceptable_open_percentage_difference

    def analyze(self, crypto):
        # sell if ( (get_rating(currency).FCAS_SCORE << yesterday_rating.FCAS_SCORE) && (rating.FCAS_Score > 800) && (PriceVSOpen < 2%) && STOP_LOSS == True )
        # buy if ( (get_rating(currency).FCAS_SCORE >> yesterday_rating.FCAS_SCORE) && (PriceVSOpen > 2%) )
        # take into account books with trending and ratio parameters

        print(crypto)

        # Query the currency's collection to get today's and yesterday's ratings from MongoDB
        today = date.today()
        yesterday = today - timedelta(days=1)

        rating_today = crypto.rating.filter_by_date(today)
        rating_yesterday = crypto.rating.filter_by_date(yesterday)

        rating = None
        if rating_today is None:
            logging.info("Saving rating for Today")
            alpha = AlphaVantage(self.currency.split("-")[0])
            alpha.get_crypto_rating(crypto)
            crypto.rating.save_to_db()
            logging.info("Rating saved: %s", str(crypto.rating))
            rating_today = crypto.rating.filter_by_date(today)

        if rating_today is not None and rating_yesterday is not None:
            rating = float(rating_today["FCAS_Score"]) - float(rating_yesterday["FCAS_Score"])

        rating = float(rating_today["FCAS_Score"]) - float(rating_yesterday["FCAS_Score"]) if rating_today is not None and rating_yesterday is not None else None
        print(rating)

        # Check what's the different % between current Price and Open
        price_vs_open = crypto.percent_open()
        print(price_vs_open)

        stop_loss = self.stop_loss(crypto)
        print(stop_loss)

        if (rating is not None and rating < self.acceptable_score_difference * -1 ) \
            and price_vs_open < self.acceptable_open_percentage_difference * -1 \
            and stop_loss:
                self.sell_flag = True

        if (rating is not None and rating > self.acceptable_score_difference) \
            and (rating_today is not None and rating_today["FCAS_Score"] > 800) \
            and price_vs_open > self.acceptable_open_percentage_difference:
                self.buy_flag = True

        print("SELL FLAG = " + str(self.sell_flag))
        print("BUY FLAG = " + str(self.buy_flag))


    def stop_loss(self, crypto):
        # STOP_LOSS is True if (current_price < lower_limit where lower_limit = upper_limit - upper_limit * acceptable_percentage) Acceptable_percentage default = 2%
        # if the value goes up, the lower_limit keeps increasing, but if the value goes down, lower_limit does not change

        current_value_limit = crypto.price * (1 - self.acceptable_percentage/100)

        if self.lower_limit < current_value_limit:
            self.lower_limit = current_value_limit

        logging.info("Current value limit: %s\nLower limit: %s\nAcceptable percentage: %s", current_value_limit, self.lower_limit, self.acceptable_percentage)

        if crypto.price < self.lower_limit:
            return True

        return False
