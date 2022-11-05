import aiohttp, requests, json, asyncio
import websockets
import threading
import queue
import nest_asyncio
nest_asyncio.apply()


async def fetch_ftx_market_data_async():
    """ Fetch market data from ftx. 

    Returns:
        dict: ['PAIR'] [name', 'enabled', 'postOnly', 'priceIncrement', 'sizeIncrement', 'minProvideSize', 'last', 'bid', 'ask', 'price', 
        'type', 'futureType', 'baseCurrency', 'isEtfMarket', 'quoteCurrency', 'underlying', 'restricted', 'highLeverageFeeExempt', 
        'largeOrderThreshold', 'change1h', 'change24h', 'changeBod', 'quoteVolume24h', 'volumeUsd24h', 'priceHigh24h', 'priceLow24h]
    """
    url = "https://ftx.com/api/markets"
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


async def fetch_all_ftx_market():
    """ Returns all market from ftx.

    Returns:
        list: List of all market from ftx markets.
    """
    url = "https://ftx.com/api/markets"
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


async def fetch_ftx_orderbook(market):
    url = f"https://ftx.com/api/markets/{market}/orderbook"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            resp = await response.text()
            results = json.loads(resp)
            return results


async def ftx_subscribe(channel, market):
    url = 'wss://ftx.com/ws/'
    params = json.dumps({"op": "subscribe", "channel": channel, "market": market})
    async with websockets.connect(url) as websocket:
        await websocket.send(params)
        try:
            while True:
                print(await websocket.recv())
        except KeyboardInterrupt as e:
            websocket.send(json.dumps({"op": "unsubscribe", "channel": channel, "market": market}))
            print(await websocket.recv())



asyncio.run(ftx_subscribe("ticker", "BTC-PERP"))



async def run_every(x, func):
    await asyncio.sleep(x)
    return await func()
    


# data = asyncio.get_event_loop().run_until_complete(run_every(1, fetch_ftx_market_data_async))
# print(data['BTC-PERP']['last'])

# data = asyncio.get_event_loop().run_until_complete(fetch_all_ftx_market())
# print(data)