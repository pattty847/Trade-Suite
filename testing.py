import ccxt.async_support as ccas
from asyncio import run, gather

async def fetch_ohlcv(exchange, symbol, timeframe, limit):
    since = None
    while True:
        try:
            ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, since, limit)
            if len(ohlcv):
                first_candle = ohlcv[0]
                datetime = exchange.iso8601(first_candle[0])
                print(first_candle[1:][3])
        except Exception as e:
            print(type(e).__name__, str(e))


async def main():
    exchange = ccas.binance()
    timeframe = '1m'
    limit = 1
    symbols = ['BTC/USDT']
    loops = [fetch_ohlcv(exchange, symbol, timeframe, limit) for symbol in symbols]
    await gather(*loops)
    await exchange.close()


run(main())