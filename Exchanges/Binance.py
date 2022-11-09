import time
import aiohttp
import json
import asyncio
import websockets
import threading
import queue
import sched
import dearpygui.dearpygui as dpg
import nest_asyncio
nest_asyncio.apply()


REST_ENDPOINT = "https://api.binance.com"

WEBSOCKET_ENDPOINT = "wss://stream.binance.com:9443 "

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

active_websocket_connections = dict()


async def _get(endpoint: str, **kwargs):
    """ This is the based get request for any call to the Binance API.

    Args:
        endpoint (str): API endpoint ex: /api/v3/exchangeInfo
        args (endpoint key/value): Paramters for the endpoint specified.

    Returns:
        json: Returns json response from the exchange.
    """

    # Create our full url based on endpoint passed
    url = f"{REST_ENDPOINT}{endpoint}"
    # If arguments were passed include them in the params
    args = kwargs if kwargs else ""

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers = {'content-type': 'application/json'}, params = args) as response:
            if response.status == 200:
                resp = await response.json()
                return "status: 200"
            else:
                print(f"Error code: {response.status}")


async def websocket_handler():
    pass


def sub_to_websocket(*args):
    for ticker in args:
        active_websocket_connections[ticker] = 


sub_to_websocket("BTC-USDT", "ETH-USDT", "XXX")


def create_schedule(delay, priority, action):
    s = sched.scheduler(time.time, time.sleep)
    action = asyncio.run(action)
    s.enter(delay, priority, action)
    s.run()


# data = asyncio.run(_get("/api/v3/exchangeInfo"))
# if data:
#     print(data)


# create_schedule(3, 1, _get("/api/v3/exchangeInfo"))