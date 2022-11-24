from asyncio import gather
import asyncio
import datetime
import os
import ccxt.async_support as ccas
import ccxt
import dearpygui.dearpygui as dpg
import pandas as pd

msec = 1000
minute = 60 * msec
hold = 30


async def retry_fetch_candles(api, max_retries:int, symbol: str, timeframe: str, since: str, limit: int):
    num_retries = 0
    try:
        num_retries += 1
        try: 
            ohlcv = await api.fetch_ohlcv(symbol, timeframe, since, limit)
        except ccxt.ExchangeError as e:
            print(e)
        # print('Fetched', len(ohlcv), symbol, 'candles from', api.iso8601 (ohlcv[0][0]), 'to', api.iso8601 (ohlcv[-1][0]))
        return ohlcv
    except Exception:
        if num_retries > max_retries:
            raise  # Exception('Failed to fetch', timeframe, symbol, 'OHLCV in', max_retries, 'attempts')


async def fetch_candles(exchange: str, max_retries:int, symbol: str, timeframe: str, since: str, limit: int, dataframe: bool):
    # TODO: Add to this function a way check if there exists a file for this exchange, symbol, timeframe and if so,
    # update the fetch since to the last timeframe in the file, update the file, and then return all_ohlcv

    exchange = getattr(ccas, exchange)()

    timeframe_duration_in_seconds = exchange.parse_timeframe(timeframe)
    timeframe_duration_in_ms = timeframe_duration_in_seconds * 1000
    timedelta = limit * timeframe_duration_in_ms
    
    # This will always be the current time unless updating OLD candles using the TO var where TO is first_pull_time in CSV file
    now = exchange.milliseconds()
    all_ohlcv = []
    fetch_since = exchange.parse8601(since)

    
    while fetch_since < now:
        
        ohlcv = await retry_fetch_candles(exchange, max_retries, symbol, timeframe, fetch_since, limit)
        if ohlcv is None:
            await exchange.close()
            return None
        fetch_since = (ohlcv[-1][0] + 1) if len(ohlcv) else (fetch_since + timedelta)
        all_ohlcv = all_ohlcv + ohlcv
        
        if len(all_ohlcv):
            print(len(all_ohlcv), 'candles in total from', exchange.iso8601(all_ohlcv[0][0]), 'to', exchange.iso8601(all_ohlcv[-1][0]))
        
        else:
            print(len(all_ohlcv), 'candles in total from', exchange.iso8601(fetch_since))
            
    await exchange.close()
    return all_ohlcv if not dataframe else pd.DataFrame(all_ohlcv)



async def fetch_latest_candles(candles, exchange, symbol, timeframe):
    """ TODO: This function will fetch the latest candles since the last time saved in the local storage for an exchange, symbol, and timeframe.


    Args:
        candles (dict): Candlestick data that was saved and loaded.
        exchange (str): Name of the exchange.
        symbol (str): Symbol.
        timeframe (str): Timeframe.
    """
    api = getattr(ccas, exchange)()

    columns = ['date', 'open', 'high', 'low', 'close', 'volume']

    # If the file exists load it
    old_candles = pd.DataFrame(candles)
    last_pull_time = old_candles.iat[-1, 0] # last stored time

    # This part grabs new candles since last_pull_time and drops the first row because its a duplicate.
    new_candles = pd.DataFrame(fetch_candles(3, symbol, timeframe, last_pull_time, 500), columns=columns)
    new_candles.drop(new_candles.head(1).index, inplace=True)
    
    # We will concat the new candles with the old candles
    new_ohlcv = pd.concat([old_candles, new_candles], ignore_index=True)

    # TODO: Write a method to save the new_ohlcv to its respective fille

    # Return all the candles
    return new_ohlcv

    
def get_orders(exchange:str, symbol:str, since:str):
    market = exchange.market(symbol)
    one_hour = 3600 * 1000
    since = exchange.parse8601(since)
    now = exchange.milliseconds()
    end = exchange.parse8601(exchange.ymd(now) + 'T00:00:00')
    previous_trade_id = None
    filename = "CSV\\" + exchange.id + '\\' + market['id'].replace('/', '').lower() + '-orders.csv'
    all_orders = []
    while since < end:
        try:
            trades = exchange.fetch_trades(symbol, since)
            print(exchange.iso8601(since), len(trades), 'trades')
            if len(trades):
                last_trade = trades[-1]
                if previous_trade_id != last_trade['id']:
                    since = last_trade['timestamp']
                    previous_trade_id = last_trade['id']
                    for trade in trades:
                        all_orders.append({
                            'timestamp': trade['timestamp'],
                            'size': trade['amount'],
                            'price': trade['price'],
                            'side': trade['side'],
                        })
                else:
                    since += one_hour
            else:
                since += one_hour
        except ccxt.NetworkError as e:
            print(type(e).__name__, str(e))
            exchange.sleep(60000)
    df = pd.DataFrame(all_orders, columns=["timestamp", "size", "price", "side"])
    return df


async def fetch_trades(exchange, symbol):
    minute = 60000
    hour = minute * 60
    day = hour * 24


    api = getattr(ccas, exchange)()
    now = api.milliseconds()
    data = await api.fetch_trades(symbol, now - minute)
    df = pd.DataFrame(data).to_csv("trades.csv")
    print (df)
    await api.close()



# print(asyncio.run(fetch_trades("binance", "BTCUSDT")))