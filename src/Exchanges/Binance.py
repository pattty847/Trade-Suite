import time
import aiohttp
import json
import asyncio
import websockets
import threading
import queue
import schedule
import dearpygui.dearpygui as dpg
import nest_asyncio

nest_asyncio.apply()


REST_ENDPOINT = "https://api.binance.com"

WEBSOCKET_ENDPOINT = "wss://stream.binance.com:9443/ws"

timeframes = {
    '1s': '1s',  # spot only for now
    '1m': '1m',
    '3m': '3m',
    '5m': '5m',
    '15m': '15m',
    '30m': '30m',
    '1h': '1h',
    '2h': '2h',
    '4h': '4h',
    '6h': '6h',
    '8h': '8h',
    '12h': '12h',
    '1d': '1d',
    '3d': '3d',
    '1w': '1w',
    '1M': '1M',
}

active_websocket = []

async def _get(endpoint: str, kwargs):
    """ This is the based get request for any call to the Binance API.

    Args:
        endpoint (str): API endpoint ex: /api/v3/exchangeInfo
        args (endpoint key/value): Paramters for the endpoint specified.

    Returns:
        json: Returns json response from the exchange.
    """

    # Create our full url based on endpoint passed
    url = f"{REST_ENDPOINT}{endpoint}"
    # If arguments were passed include them in the params else empty string
    args = kwargs if kwargs else ""

    # Create ClinetSession
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"Accepts" : "application/json"}, params = args) as response:
            if response.status == 200:
                resp = await response.json()
                return resp
            else:
                print(f"Error code: {response.status}")
                return None


async def fetch_candles(ticker, timeframe, chart_id, viewport_width, viewport_height, start_time=None, end_time=None, limit=1000):

    dpg.add_loading_indicator(circle_count=5, parent=chart_id, tag="loading", pos=[viewport_width/2, viewport_height/2 - 110], radius=10.0)
    
    if start_time:
        params = {"symbol":ticker, "interval": timeframe, "startTime": start_time, "endTime":end_time, "limit":limit}
    else:
        params = {"symbol":ticker, "interval": timeframe, "limit":1000}

    candles = await _get(endpoint="/api/v3/klines", kwargs = params)


    time, open, high, low, close, volume = [],[],[],[],[],[]
    if candles:
        for row in candles:
            time.append(float(row[0])/1000)
            open.append(float(row[1]))
            high.append(float(row[2]))
            low.append(float(row[3]))
            close.append(float(row[4]))
            volume.append(float(row[5]))
    return {"time":time, "open":open, "high":high, "low":low, "close":close, "volume":volume}



async def fetch_order_book(ticker, limit):
    params = {"symbol":ticker, "limit":limit}
    return await _get("/api/v3/depth", params)


async def sub_to_websocket(*args):
    """ Args are endpoints from binance you would like to subscribe to: btcusdt@aggTrade, ethusdt@kline5m, etc
    """
    [active_websocket.append(x) for x in args]
    params = {
        "method": "SUBSCRIBE",
        "params": [x for x in args],
        "id": 1
    }
    print(f"Subscribing to {active_websocket}")
    async with websockets.connect(WEBSOCKET_ENDPOINT) as websocket:
        await websocket.send(json.dumps(params))
        try:
            while True:
                message = json.loads(await websocket.recv())
                print(type(message))
                print(message)
                print(f"time:{message['E']} - {message['s']}: ${message['p'] : message['q']}")


        except Exception as e:
            print(e)
        
        finally:
            print(f"Closing websockets {args}")
            websocket.send(json.dumps({
                "method": "UNSUBSCRIBE",
                "params": [x for x in args],
                "id": 2
            }))
            print(await websocket.recv())