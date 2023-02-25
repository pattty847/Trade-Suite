import os
import json
import pandas as pd
import ccxt
import ccxt.pro as ccxtpro
import asyncio


def save_candles_to_file(exchange, symbol, timeframe, candles):
    symbol = symbol.replace("/", "_")
    directory = f"exchanges/candles/{exchange}"
    os.makedirs(directory, exist_ok=True)
    with open(f"{directory}/{symbol}_{timeframe}.json", "w") as f:
        json.dump(candles, f)


async def fetch_candles(
    exchange: str,
    symbol: str,
    timeframe: str,
    since: str,
    limit: int,
    dataframe: bool,
    chart_tag: str,
    max_retries=3,
):
    api = getattr(ccxtpro, exchange)()
    filename = (
        f"exchanges/candles/{exchange}/{symbol.replace('/', '_')}_{timeframe}.json"
    )
    candles = (
        json.load(open(filename, "r"))
        if os.path.exists(filename)
        else {"time": [], "open": [], "high": [], "low": [], "close": [], "volume": []}
    )

    fetched_candles = []
    timeframe_duration_in_seconds = api.parse_timeframe(timeframe)
    timedelta = limit * timeframe_duration_in_seconds * 1000
    now = api.milliseconds()

    fetch_since = (
        api.parse8601(since)
        if not len(candles["time"])
        else int(candles["time"][-1] * 1000)
    )
    while True:
        candle_batch = None
        for num_retries in range(max_retries):
            try:
                candle_batch = await api.fetch_ohlcv(
                    symbol, timeframe, since=fetch_since, limit=limit
                )
            except ccxt.ExchangeError as e:
                print(e)
                await asyncio.sleep(1)
            if candle_batch is not None:
                break
        if candle_batch is None:
            await api.close()
            return None

        fetched_candles += candle_batch

        if len(candle_batch):
            last_time = candle_batch[-1][0] + timeframe_duration_in_seconds * 1000
            print(
                len(candle_batch),
                "candles from",
                api.iso8601(candle_batch[0][0]),
                "to",
                api.iso8601(candle_batch[-1][0]),
            )
        else:
            last_time = fetch_since + timedelta
            print("no candles")

        if last_time >= now:
            break

        fetch_since = last_time

    for row in fetched_candles[1:]:
        candles["time"].append(row[0] / 1000)
        candles["open"].append(float(row[1]))
        candles["high"].append(float(row[2]))
        candles["low"].append(float(row[3]))
        candles["close"].append(float(row[4]))
        candles["volume"].append(float(row[5]))

    save_candles_to_file(exchange, symbol, timeframe, candles)

    await api.close()
    return pd.DataFrame(candles) if dataframe else candles
