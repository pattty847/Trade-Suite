import json
import os
import ccxt
import pandas as pd
import ccxt.pro as ccxtpro
import asyncio

async def retry_fetch_candles(api, max_retries: int, symbol: str, timeframe: str, since: str, limit: int):
    num_retries = 0
    while num_retries < max_retries:
        try:
            ohlcv = await api.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
            return ohlcv
        except ccxt.ExchangeError as e:
            print(e)
            num_retries += 1
            await asyncio.sleep(1)
    return None

def save_candles_to_file(exchange, symbol, timeframe, candles):
    symbol = symbol.replace("/", "_")
    directory = f"exchanges/candles/{exchange}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(f"{directory}/{symbol}_{timeframe}.json", "w") as f:
        f.write(json.dumps(candles))

async def fetch_candles(exchange: str, symbol: str, timeframe: str, since: str, limit: int, dataframe: bool, max_retries=3):
    api = getattr(ccxtpro, exchange)()

    timeframe_duration_in_seconds = api.parse_timeframe(timeframe)
    timedelta = limit * timeframe_duration_in_seconds * 1000

    if os.path.exists(f"exchanges/candles/{exchange}/{symbol.replace('/', '_')}_{timeframe}.json"):
        with open(f"exchanges/candles/{exchange}/{symbol.replace('/', '_')}_{timeframe}.json", "r") as f:
            candles = json.load(f)
        return candles if not dataframe else pd.DataFrame(candles)

    all_ohlcv = []

    now = api.milliseconds()
    fetch_since = api.parse8601(since)

    while True:
        ohlcv = await retry_fetch_candles(api, max_retries, symbol, timeframe, fetch_since, limit)

        if ohlcv is None:
            await api.close()
            return None

        all_ohlcv += ohlcv

        if len(ohlcv):
            last_time = ohlcv[-1][0] + timeframe_duration_in_seconds * 1000
            print(len(ohlcv), 'candles from', api.iso8601(ohlcv[0][0]), 'to', api.iso8601(ohlcv[-1][0]))
        else:
            last_time = fetch_since + timedelta
            print('no candles')

        if last_time >= now:
            break

        fetch_since = last_time

    candles = {"time": [], "open": [], "high": [], "low": [], "close": [], "volume": []}
    for row in all_ohlcv:
        candles['time'].append(row[0]/1000)
        candles['open'].append(float(row[1]))
        candles['high'].append(float(row[2]))
        candles['low'].append(float(row[3]))
        candles['close'].append(float(row[4]))
        candles['volume'].append(float(row[5]))

    save_candles_to_file(exchange, symbol, timeframe, candles)

    await api.close()
    return candles if not dataframe else pd.DataFrame(candles)