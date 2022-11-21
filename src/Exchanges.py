import ccxt.async_support as ccxt

class Exchange:

    def __init__(self) -> None:
        self.apis = {}
        for exchange in ccxt.exchanges:
            self.apis[exchange] = getattr(ccxt, exchange)