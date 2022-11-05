import os
import ccxt as ccxt
import ccxt.async_support as ccas
import asyncio
import pandas as pd
import dearpygui.dearpygui as dpg

def retry_fetch_ohlcv(max_retries:int, exchange:str, symbol: str, timeframe: str, since: str, limit: int):
    num_retries = 0
    try:
        num_retries += 1
        try: 
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
        except ccxt.ExchangeError as e:
            print(e)
        # print('Fetched', len(ohlcv), symbol, 'candles from', exchange.iso8601 (ohlcv[0][0]), 'to', exchange.iso8601 (ohlcv[-1][0]))
        return ohlcv
    except Exception:
        if num_retries > max_retries:
            raise  # Exception('Failed to fetch', timeframe, symbol, 'OHLCV in', max_retries, 'attempts')


def scrape_ohlcv(max_retries:int, exchange:str, symbol: str, timeframe: str, since: str, limit: int):

    timeframe_duration_in_seconds = exchange.parse_timeframe(timeframe)
    timeframe_duration_in_ms = timeframe_duration_in_seconds * 1000
    timedelta = limit * timeframe_duration_in_ms
    
    # This will always be the current time unless updating OLD candles using the TO var where TO is first_pull_time in CSV file
    now = exchange.milliseconds()
    all_ohlcv = []
    fetch_since = since
    
    while fetch_since < now:
        
        ohlcv = retry_fetch_ohlcv(max_retries, exchange, symbol, timeframe, fetch_since, limit)

        fetch_since = (ohlcv[-1][0] + 1) if len(ohlcv) else (fetch_since + timedelta)
        all_ohlcv = all_ohlcv + ohlcv
        
        if len(all_ohlcv):
            print(len(all_ohlcv), 'candles in total from', exchange.iso8601(all_ohlcv[0][0]), 'to', exchange.iso8601(all_ohlcv[-1][0]))
        
        else:
            print(len(all_ohlcv), 'candles in total from', exchange.iso8601(fetch_since))
    
    return exchange.filter_by_since_limit(all_ohlcv, since, None, key=0)


def get_candles(exchange: str, symbol: str, timeframe: str, since: str, chart_id, viewport_width, viewport_height):
    
    dpg.add_loading_indicator(circle_count=4, parent=chart_id, tag="loading", pos=[viewport_width/2, viewport_height/2 - 110], radius=10.0)

    columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    sym = symbol.replace('/', '').lower() # remove /
    exch = str(exchange).replace(" ", "").lower() # remove spaces, lowercase
    dir_ = f'data\\{exch}'                                                           # build directory: CSV/exchange/
    file = f'{dir_}\\{sym}-{timeframe}.csv'                                           # build file: CSV/exchange/btcusdt-5m.csv
    since = exchange.parse8601(since)

    if not os.path.exists(dir_): # make directory if it doesn't exist
        os.mkdir(dir_)

    if not (os.path.isfile(file)): # make file if it doesn't exist
        ohlcv = scrape_ohlcv(3, exchange, symbol, timeframe, since, 500)
        if len(ohlcv):
            ohlcv = pd.DataFrame(ohlcv, columns=columns) # pull ohlcv data
            ohlcv.to_csv(file, mode='w', index=False) # write to CSV file. 

        return pd.DataFrame(ohlcv, columns=columns)

    # If the file exists load it
    old_candles = pd.read_csv(file)
    first_pull_time = old_candles.iat[0, 0] # first stored time
    last_pull_time = old_candles.iat[-1, 0] # last stored time

    # This part grabs new candles since last_pull_time and drops the first row because its a duplicate.
    new_candles = pd.DataFrame(scrape_ohlcv(3, exchange, symbol, timeframe, last_pull_time, 500), columns=columns)
    new_candles.drop(new_candles.head(1).index, inplace=True)
    
    # We will conate the new candles with the old candles
    new_ohlcv = pd.concat([old_candles, new_candles], ignore_index=True)

    # Append the newest candles to their respective file
    new_candles.to_csv(file, mode='a', index=False, header=False)

    # Return all the candles
    return new_ohlcv


# TODO: Create function that scans for spreads between assets

# TODO: Create function that pulls orders from each exchange if they have that option. 


def get_orders(exchange: str, symbol: str, since: str):
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

# bin = getattr(ccxt, "binance")()
# bin.load_markets()
# print(get_orders(bin, "BTC/USDT", "2022-11-02T21:00:00Z"))


def get_candles_from_csv(self, exchange: str, symbol: str, timeframe: str):
    columns=['date', 'open', 'high', 'low', 'close', 'volume']
    sym = symbol.replace('/', '').lower()
    file = f'CSV\\{str(self.exchange).replace(" ", "").lower()}-{sym}-{timeframe}.csv'
    df = pd.read_csv(file)
    df.columns = columns
    return df


def get_multi_candles(self, exchange: str, tickers:list, timeframe:str, since:str):
    """ This function will return a dictionary of dataframe object(s) where the key is the ticker. It will loop through the tickers passed to it
        and call the get_candles() function, storing or updating the data in the CSV folder. 

    Args:
        tickers (list): list of ticker pairs to fetch
        timeframe (str): a single timeframe
        since (str): timestamp of when to start fetching candles from

    Returns:
        dict: a returned dictionary containing the candlestick dataframe accessable by the ticker as a key
    """
    candles = {}
    if len(tickers) == 1:
        df = self.get_candles(tickers[0])
        return df
    for ticker in tickers:
        df = self.get_candles(ticker, timeframe, since)
        candles[ticker] = df
    return candles


def get_matrix_of_closes(self, exchange: str, tickers:list, timeframe:str, since:str):
    """This will generate a matrix of ticker closes from since to now by a certain timeframe. 

    Args:
        tickers (list): list of ticker pairs to fetch
        timeframe (str): a single timeframe
        since (str): timestamp of when to start fetching candles from

    Returns:
        DataFrame: it will return a dataframe of these closes 
    """
    ohlcv = self.get_multi_candles(tickers, timeframe, since)
    df = pd.DataFrame()
    for ticker in ohlcv.keys():
        df[ticker] = ohlcv[ticker]['close']
    # df.index = ohlcv[df.columns.tolist()[0]]['date']
    return df