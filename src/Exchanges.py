import ccxt.async_support as ccxt


# TODO: Testing exchange objects that can be an extension of individual exchanges like Binance -> extends -> (Exchange)
class Exchange:

    def __init__(self) -> None:
        self.apis = {}
        for exchange in ccxt.exchanges:
            self.apis[exchange] = getattr(ccxt, exchange)