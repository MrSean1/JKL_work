import logging

from websocket import create_connection
import gzip
import time


class HuoBiWebsocket:
    def __init__(self, endpoint, symbol, api_key=None, api_secret=None, ):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing WebSocket.")
        self.endpoint = endpoint
        self.symbol = symbol
        if api_key is not None and api_secret is None:
            raise ValueError('api_secret is required if api_key is provided')
        if api_key is None and api_secret is not None:
            raise ValueError('api_key is required if api_secret is provided')
        self.api_key = api_key
        self.api_secret = api_secret
        self.data = {}
        self.exited = False

