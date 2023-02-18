import dearpygui.dearpygui as dpg
import ccxt.pro as ccxt
import pandas as pd
from asyncio import run 


async def push_orderbook_panel(sender, app_data, user_data):

    async def fetch_data():
        done = False
        cbp = ccxt.coinbasepro({"newUpdates": True})
        cb = ccxt.coinbaseprime({"newUpdates": True})
        while not done:
            cbp_orderbook = await cbp.watch_order_book("ETH-USDT")
            cb_orderbook = await cb.watch_order_book("ETH-USDT")
            
            cbp_bids = cbp_orderbook['bids']
            cbp_asks = cbp_orderbook['asks']
            print(cbp_bids)

            done = True
        await cbp.close()
        await cb.close()


    await fetch_data()