"""Execute processes in the system"""
import argparse
from coin.coinbase import Coinbase

parser = argparse.ArgumentParser(description="Communicate with your Crypto Account throgh this CLI")
parser.add_argument("--currency", default="BTC", help="Crypto Currency Name")
args = parser.parse_args()

c = Coinbase(args.currency)
crypto = c.get_current()
print(crypto)
