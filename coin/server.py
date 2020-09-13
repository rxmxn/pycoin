"""Execute processes in the system"""
import time
import logging
import json
from flask import Flask, request, jsonify
from coin.coinbase import Coinbase
from coin.alphavantage import AlphaVantage
from coin.coin import Coin
from coin.websocket import WSClient


app = Flask(__name__)
wsc = WSClient()

class Server():
    def start_server(self):
        """Communicate with your Crypto Account throgh this Server"""
        logging.basicConfig(filename='pycoin.log', level=logging.INFO)
        logging.info('Starting PyCoin')
        app.run(debug=True)

    @app.route('/start-websocket/<currency>', methods=['GET'])
    def start_websocket(currency):
        wsc.start(currency)
        return jsonify({"Message": "WebSocket Started"})

    @app.route('/stop-websocket', methods=['GET'])
    def stop_websocket():
        wsc.stop()
        return jsonify({"Message": "WebSocket is Closed"})

