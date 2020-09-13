"""Analytics class to run the logic to do transactions"""
import time
import logging
from datetime import datetime, date, timedelta
from coin.coin import Coin
from coin.alphavantage import AlphaVantage


class Analytics:
    def __init__(self, currency):
        self.currency = currency

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

    def stop_loss(self, crypto):
        # STOP_LOSS is True if (current_price < lower_limit where lower_limit = upper_limit - upper_limit * acceptable_percentage) Acceptable_percentage default = 2%
        # if the value goes up, the lower_limit keeps increasing, but if the value goes down, lower_limit does not change

        return True
