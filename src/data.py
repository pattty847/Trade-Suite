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

def load_candles_from_file(exchange, symbol, timeframe):
    filename = (
        f"exchanges/candles/{exchange}/{symbol.replace('/', '_')}_{timeframe}.json"
    )
    return (
        json.load(open(filename, "r"))
        if os.path.exists(filename)
        else {"dates": [], "opens": [], "highs": [], "lows": [], "closes": [], "volumes": []}
    )


async def fetch_candles(
    exchange: str,
    symbol: str,
    timeframe: str,
    since: str,
    limit: int,
    dataframe: bool,
    max_retries=3,
):
    api = getattr(ccxtpro, exchange)()

    old_candles = load_candles_from_file(exchange, symbol, timeframe)

    new_candles = []
    timeframe_duration_in_seconds = api.parse_timeframe(timeframe)
    timedelta = limit * timeframe_duration_in_seconds * 1000
    now = api.milliseconds()

    fetch_since = (
        api.parse8601(since)
        if not len(old_candles["dates"])
        else int(old_candles["dates"][-1] * 1000)
    )
    
    while True:
        new_candle_batch = None
        for num_retries in range(max_retries):
            try:
                new_candle_batch = await api.fetch_ohlcv(
                    symbol, timeframe, since=fetch_since, limit=limit
                )
            except ccxt.ExchangeError as e:
                print(e)
                await asyncio.sleep(1)
            if new_candle_batch is not None:
                break
        if new_candle_batch is None:
            await api.close()
            return None

        new_candles += new_candle_batch

        if len(new_candle_batch):
            last_time = new_candle_batch[-1][0] + timeframe_duration_in_seconds * 1000
            print(len(new_candle_batch), "candles from", api.iso8601(new_candle_batch[0][0]), "to", api.iso8601(new_candle_batch[-1][0]))
        else:
            last_time = fetch_since + timedelta
            print("no candles")

        if last_time >= now:
            break

        fetch_since = last_time

    for row in new_candles[1:]:
        old_candles["dates"].append(row[0] / 1000)
        old_candles["opens"].append(float(row[1]))
        old_candles["highs"].append(float(row[2]))
        old_candles["lows"].append(float(row[3]))
        old_candles["closes"].append(float(row[4]))
        old_candles["volumes"].append(float(row[5]))

    save_candles_to_file(exchange, symbol, timeframe, old_candles)

    await api.close()
    return pd.DataFrame(old_candles) if dataframe else old_candles


async def fetch(exchange_name, symbol, limit):
    exchange_class = getattr(ccxtpro, exchange_name)
    exchange = exchange_class(
        {
            "enableRateLimit": True,  # add rate limiter
            "newUpdates": True
        }
    )

    while True:
        try:
            # watch the data using the specified method
            orderbook = await getattr(exchange, "watchOrderBook")(symbol, limit)
            # trades = await getattr(exchange, "watchTrades")(symbol)

            if orderbook['bids'] and orderbook['asks']:
                # print(trades)
                print(orderbook['bids'][0], orderbook['asks'][0])

        except KeyboardInterrupt:
            print("KeyboardInterrupt detected. Closing exchange...")
            await exchange.close()
            break

    print("Exchange closed.")



# asyncio.run(fetch("coinbasepro", "BTC/USD", 1))