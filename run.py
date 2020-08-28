"""Execute processes in the system"""
import argparse
from datetime import date
from coin.coinbase import Coinbase
from coin.alphavantage import AlphaVantage

parser = argparse.ArgumentParser(description="Communicate with your Crypto Account throgh this CLI")
parser.add_argument("--currency", default="BTC", help="Crypto Currency Name")
args = parser.parse_args()

c = Coinbase(args.currency)
crypto = c.get_current()
print(crypto)

print("\nHistorics")
#cryptos = c.get_historic_rates(n_elements=300)
#print(cryptos[-1])

#hist = c.get_historic_rates()
#print(hist[-1])

start = date(2019, 12, 5).isoformat()
#end = date(2020, 1, 5).isoformat()
#hist3 = c.get_historic_rates(start=start, end=end, n_elements=300)
#print(hist3[-1])
#print(hist3[0])

a = AlphaVantage(args.currency)
cr = a.get_value_from_date(start)
print(cr)

crypto_list = a.get_historics(start="2019-01-01", end="2019-01-03")
for c in crypto_list:
    print(c)
