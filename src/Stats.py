import dearpygui.dearpygui as dpg
import utils.DoStuff as do
import pandas as pd
import os
import asyncio
import aiohttp


def fetch_cmc():
    from requests import Request, Session
    from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
    import json

    url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'1',
    'limit':'5000',
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '31c20493-3635-494b-852a-904ffb636906',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

print(fetch_cmc())


async def fetch_coinmarketcap(limit: str, currency: str):
    API_KEY = "31c20493-3635-494b-852a-904ffb636906"
    URL = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    PARAMS = {
    'start':'1',
    'limit':limit,
    'convert':currency
    }
    HEADERS = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(URL, headers = HEADERS, params = PARAMS) as response:
            print(response.status)
            print(await response.text())

# asyncio.run(fetch_coinmarketcap("5000", "USD"))

def fetch_coinalyze():
    URL = 'https://coinalyze.net/'
    columns = ["Coin", "Price", "Chg 24H", "Vol 24H", "Open Interest", "OI Chg 24H", "OI Share", "OI / VOL24H", "FR AVG", "PFR AVG", "Liqs. 24H"]
    stats = pd.read_html(URL)[0][columns]
    
    try:
        with open("src\\Exchanges\\CSV\\previous_stats.csv", "r"):
            previous_stats = pd.read_csv("src\\Exchanges\\CSV\\previous_stats.csv")
    except FileNotFoundError as e:
        stats.to_csv(f"src\\Exchanges\\CSV\\previous_stats.csv", index=False)
        previous_stats = None
    
    return (stats, previous_stats, columns)

def push_stats_panel(sender, primary_window_width):

    market_stats, previous_stats, columns = fetch_coinalyze()

    with dpg.window(label="Crypto Stats", tag="stats-window", width=800, height=1000, pos=[15, 60], on_close = lambda sender: dpg.delete_item(sender)):
        
        with dpg.table(tag='stats-table', borders_innerH=True, borders_innerV=True, borders_outerH=True, borders_outerV=True, resizable=True, sortable=True, callback=do.sort_callback):
            
            for col in columns:                                       # Generates the correct amount of columns
                dpg.add_table_column(label=col)                       # Adds the headers

            
            
            for i in range(market_stats.shape[0]):                    # Shows the first n rows
                
                with dpg.table_row():
                    
                    for j in range(market_stats.shape[1]):
                        
                        dpg.add_text(f"{market_stats.iloc[i,j]}")