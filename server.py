"""Execute processes in the system"""
import time
import logging
import json
from flask import Flask, request, jsonify
from coin.coinbase import Coinbase
from coin.alphavantage import AlphaVantage
from coin.coin import Coin
from coin.websocket import myWebsocketClient

app = Flask(__name__)

def start_server():
    """Communicate with your Crypto Account throgh this Server"""
    logging.basicConfig(filename='pycoin.log', level=logging.INFO)
    logging.info('Starting PyCoin')
    app.run(debug=True)

@app.route('/start-websocket/<currency>', methods=['GET'])
def start_websocket(currency):
    wsClient = myWebsocketClient()
    wsClient.set_currency(currency)
    wsClient.start()

    print(wsClient.url, wsClient.products)

    while (wsClient.message_count < 5):
        print ("\nmessage_count =", "{} \n".format(wsClient.message_count))
        time.sleep(1)

    wsClient.close()

    return jsonify({"Message": "WebSocket is Closed"})


if __name__ == '__main__':
    start_server()
