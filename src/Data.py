from asyncio import gather
import asyncio
import ccxt.async_support as ccas
import ccxt  
import dearpygui.dearpygui as dpg


msec = 1000
minute = 60 * msec
hold = 30


async def retry_fetch_ohlcv(api, max_retries:int, symbol: str, timeframe: str, since: str, limit: int):
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


async def scrape_ohlcv(api, max_retries:int, symbol: str, timeframe: str, since: str, limit: int):

    api = getattr(ccas, api)()

    timeframe_duration_in_seconds = api.parse_timeframe(timeframe)
    timeframe_duration_in_ms = timeframe_duration_in_seconds * 1000
    timedelta = limit * timeframe_duration_in_ms
    
    # This will always be the current time unless updating OLD candles using the TO var where TO is first_pull_time in CSV file
    now = api.milliseconds()
    all_ohlcv = []
    fetch_since = api.parse8601(since)

    
    while fetch_since < now:
        
        ohlcv = await retry_fetch_ohlcv(api, max_retries, symbol, timeframe, fetch_since, limit)
        if ohlcv is None:
            await api.close
            return None
        fetch_since = (ohlcv[-1][0] + 1) if len(ohlcv) else (fetch_since + timedelta)
        all_ohlcv = all_ohlcv + ohlcv
        
        if len(all_ohlcv):
            print(len(all_ohlcv), 'candles in total from', api.iso8601(all_ohlcv[0][0]), 'to', api.iso8601(all_ohlcv[-1][0]))
        
        else:
            print(len(all_ohlcv), 'candles in total from', api.iso8601(fetch_since))
            
    await api.close()
    return all_ohlcv
# print(asyncio.run(scrape_ohlcv("binance", 3, "BTC/USDT", "1d", "2015-09-01 00:00:00", 500)))