import aiohttp
import json
import asyncio
import websockets
import threading
import queue
import dearpygui.dearpygui as dpg
import nest_asyncio
nest_asyncio.apply()


REST_ENDPOINT = "https://ftx.com/api"
WEBSOCKET_ENDPOINT = "wss://ftx.com/ws/"
timeframes = {
    '15s': '15',
    '1m': '60',
    '5m': '300',
    '15m': '900',
    '1h': '3600',
    '4h': '14400',
    '1d': '86400',
    '3d': '259200',
    '1w': '604800',
    '2w': '1209600',
    # the exchange does not align candles to the start of the month
    # it can only fetch candles in fixed intervals of multiples of whole days
    # that works for all timeframes, except the monthly timeframe
    # because months have varying numbers of days
    '1M': '2592000',
}


async def fetch_market_data():
    """ Fetch market data from ftx for ever market.

    Returns:
        dict['market']: Market data for all markets or ['market'].
    """
    url = f"{REST_ENDPOINT}/markets"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            resp = await response.text()
            results = json.loads(resp)
            if results["success"]:
                data = {}
                for r in results['result']:
                    name = r['name']
                    data[name] = {}
                    for k in r.keys():
                        data[name][k] = r[k]
                        await asyncio.sleep(0)
                return data
            else:
                print("failed to retieve market data...")


async def fetch_candles(market, resolution, chart_id, viewport_width, viewport_height, start_time=None, end_time=None,):
    """ Fetch candles from FTX market for resolution. Optional start_time and end_time.

    Args:
        market (str): Name of market on FTX.
        resolution (int): 15, 60, 300, 900, 3600, 14400, 86400, or any multiple of 86400 up to 30*86400
        start_time (float, optional): Filter start time. Defaults to None.
        end_time (float, optional): Filter end time. Defaults to None.

    Returns:
        list: List of lists of candle stick data [time, open, high, low, close, volume]
    """
    dpg.add_loading_indicator(circle_count=4, parent=chart_id, tag="loading", pos=[viewport_width/2, viewport_height/2 - 110], radius=10.0)
    url = f"{REST_ENDPOINT}/markets/{market}/candles"
    if start_time and end_time:
        params={"resolution":resolution, "start_time":start_time, "end_time":end_time}
    else:
        params={"resolution":resolution}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            resp = await response.text()
            results = json.loads(resp)
            if results["success"]:
                time, open, high, low, close, volume = [],[],[],[],[],[]
                for r in results['result']:
                    time.append(int(r['time'])/1000)
                    open.append(r['open'])
                    high.append(r['high'])
                    low.append(r['low'])
                    close.append(r['close'])
                    volume.append(r['volume'])
                return {"time":time, "open":open, "high":high, "low":low, "close":close, "volume":volume}
            else:
                print("failed to retieve market data...")



async def fetch_all_markets():
    """ Returns all markets from ftx (FUTURES and SPOT).
    market['type'] = "future" or "spot

    Returns:
        list: List of all markets from ftx.
    """
    url = f"{REST_ENDPOINT}/markets"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            resp = await response.text()
            results = json.loads(resp)
            if results["success"]:
                market = []
                for r in results['result']:
                    market.append(r['name'])
                return market
            else:
                print("failed to retieve market data...")


async def fetch_all_futures_markets():
    url = f"{REST_ENDPOINT}/futures"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            resp = await response.text()
            results = json.loads(resp)
            if results["success"]:
                data = {}
                for r in results['result']:
                    name = r['name']
                    data[name] = {}
                    for k in r.keys():
                        data[name][k] = r[k]
                        await asyncio.sleep(0)
                return data
            else:
                print("failed to retieve market data...")


async def fetch_market_order_book(market):
    """ Returns a certain markets orderbook.

    Args:
        market (str): market on ftx ("BTC-PERP")

    Returns:
        dict: Order book for that market.
    """
    url = f"{REST_ENDPOINT}/markets/{market}/orderbook"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            resp = await response.text()
            results = json.loads(resp)
            return results


async def subscribe_to_market(market):
    """ Starts a websocket connection which subscribes to a particular market on FTX.

    Args:
        market (str): Market from FTX.
    """
    params = json.dumps({"op": "subscribe", "channel": "ticker", "market": market})
    async with websockets.connect(WEBSOCKET_ENDPOINT) as websocket:
        await websocket.send(params)
        try:
            while True:
                print(await websocket.recv())
        except KeyboardInterrupt as e:
            websocket.send(json.dumps({"op": "unsubscribe", "channel": "ticker", "market": market}))
            print(await websocket.recv())

# asyncio.run(subscribe_to_market("BTC-PERP"))


async def subscribe_to_all_markets():
    """ Starts a websocket connection which subscribes to all market data on FTX.
    """
    params = json.dumps({"op": "subscribe", "channel": "markets"})
    async with websockets.connect(WEBSOCKET_ENDPOINT) as websocket:
        await websocket.send(params)
        try:
            while True:
                print(await websocket.recv())
        except KeyboardInterrupt as e:
            websocket.send(json.dumps({"op": "unsubscribe", "channel": "markets"}))
            print(await websocket.recv())