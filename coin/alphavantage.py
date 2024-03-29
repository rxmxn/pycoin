"""Alpha_vantage Python Client wrapper"""
import os
import logging
import sys
from datetime import date
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from coin.coin import Coin


class AlphaVantage:
    """Class to handle the AlphaVantage Python Client and to asbtract the specificities from Coin"""
    def __init__(self, currency):
        alphavantage_key = os.getenv('ALPHAVANTAGE_KEY')
        self.cc = CryptoCurrencies(key=alphavantage_key, output_format='json')
        self.currency = currency

    def get_value_from_date(self, _date):
        """Get Data from a specific date in isoformat: YYYY-MM-DD"""
        crypto = Coin(self.currency)
        data, _ = self.cc.get_digital_currency_daily(symbol=self.currency, market='USD')
        self.__parse(crypto, data[_date], _date)
        return crypto

    def __parse(self, crypto, response, _date):
        """Parse response from alphavantage into our Coin object"""
        crypto.open = response['1a. open (USD)']
        crypto.high = response['2a. high (USD)']
        crypto.low = response['3a. low (USD)']
        crypto.close = response['4a. close (USD)']
        crypto.volume = response['5. volume']
        crypto.market_cap = response['6. market cap (USD)']
        crypto.time = _date

    def get_historics(self, start=None, end=None):
        """Get historics from a currency with daily values from start date to end date"""
        coin_list = list()
        data, _ = self.cc.get_digital_currency_daily(symbol=self.currency, market='USD')

        _start = date.fromisoformat(start)
        _end = date.fromisoformat(end)

        for key, value in data.items():
            date_key = date.fromisoformat(key)
            if date_key >= _start and date_key <= _end:
                crypto = Coin(self.currency)
                self.__parse(crypto, value, key)
                coin_list.append(crypto)

        return coin_list

    def get_crypto_rating(self, crypto):
        try:
            data = self.cc.get_digital_crypto_rating(symbol=self.currency)[0]
            crypto.rating.fcas_rating = data['3. fcas rating']
            crypto.rating.fcas_score = data['4. fcas score']
            crypto.rating.developer_score = data['5. developer score']
            crypto.rating.market_maturity_score = data['6. market maturity score']
            crypto.rating.utility_score = data['7. utility score']
            crypto.rating.last_refreshed = data['8. last refreshed']
        except ValueError as err:
            print("Currency %s is currently not getting any rating, returning error: %s" % (crypto.currency, err))
        except:
            err = sys.exc_info()[0]
            logging.warning("Failed to get crypto rating with error: %s", err)
