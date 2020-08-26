"""Execute processes in the system"""
import argparse
from coin.coinbase import Coinbase
from datetime import date

parser = argparse.ArgumentParser(description="Communicate with your Crypto Account throgh this CLI")
parser.add_argument("--currency", default="BTC", help="Crypto Currency Name")
args = parser.parse_args()

c = Coinbase(args.currency)
crypto = c.get_current()
print(crypto)

print("\nHistorics")
cryptos = c.get_historic_rates(n_elements=300)
print(cryptos[-1])

hist = c.get_historic_rates()
print(hist[-1])

#check how to send dates
#start = date(2019, 12, 5).isoformat()
#print(start)
#hist3 = c.get_historic_rates(start=start, n_elements=300)
#print(hist3[-1])
