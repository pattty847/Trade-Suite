import json
import dearpygui.dearpygui as dpg
import trade_suite.utils.DoStuff as do
import pandas as pd
import os
import yfinance
import aiohttp

# TODO: Change to dict()
COIN_MARKET_CAP_ENDPOINTS = dict({
        "category":{
            "cryptocurrencies":"/cryptocurrency/",
            "exchange":"/exchange/",
            "global-metrics":"/global-metrics/",
            "tools":"/tools/",
            "blockchain":"/blockchain/",
            "fiat":"/fiat/",
            "partners":"/partners/",
            "key":"/key/",
            "content":"/content/"    
        },
        "endpoint":{
            "latest":"/latest",
            "historical":"/historical",
            "info":"/info",
            "map":"/map"
        }
    }
)


async def fetch_coinmarketcap(limit: str, currency: str, category, endpoint):
    API_KEY = "31c20493-3635-494b-852a-904ffb636906"
    URL = f'https://sandbox-api.coinmarketcap.com/v1/{category}/listings/{endpoint}'
    # TODO: Fix params to dict()
    PARAMS = {
        'start':'1',
        'limit':limit,
        'convert':currency
    }
    # TODO: Fix headers to dict()
    HEADERS = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(URL, headers = HEADERS, params = PARAMS) as response:
            print(response.status)
            response = await response.json()
            if response['data']:
                return response


def write_to_file(data, file: str):
    with open(file, "w") as f:
        json.dump(data, f)


# write_to_file(asyncio.run(fetch_coinmarketcap("100", "USD")), "coinmarketcap.csv")

def fetch_coinalyze():
    URL = 'https://coinalyze.net/'
    columns = ["Coin", "Price", "Chg 24H", "Vol 24H", "Open Interest", "OI Chg 24H", "OI Share", "OI / VOL24H", "FR AVG", "PFR AVG", "Liqs. 24H"]
    stats = pd.read_html(URL)[0][columns]

    top_ten = stats.head(10)
    
    try:
        with open("exchanges/stats/previous_stats.csv", "r"):
            previous_stats = pd.read_csv("exchanges/stats/previous_stats.csv")
    except FileNotFoundError as e:
        os.makedirs("exchanges/stats")
        stats.to_csv(f"exchanges/stats/previous_stats.csv", index=False)
        previous_stats = None
    
    return (stats, previous_stats, columns, top_ten)


def push_stats_panel():

    with open("exchanges/stats/previous_stats.csv", "r"):
        previous_stats = pd.read_csv("exchanges/stats/previous_stats.csv")

    # market_stats, previous_stats, columns, top_ten = fetch_coinalyze()
    stats = previous_stats.iloc[:, :]

    with dpg.window(label="Crypto Stats", tag="stats-window", width=800, height=1000, pos=[15, 60], on_close = lambda sender: dpg.delete_item(sender)):
        
        with dpg.tree_node(label="Top 100"):    

            with dpg.table(tag='stats-table', borders_innerH=True, borders_innerV=True, borders_outerH=True, borders_outerV=True, resizable=True, sortable=True, callback=do.sort_callback):
                
                columns = stats.iloc[:, :]



                for col in columns:                                       # Generates the correct amount of columns
                    dpg.add_table_column(label=col)                       # Adds the headers

                
                for i in range(columns.shape[0]):                    # Shows the first n rows
                    
                    with dpg.table_row():
                        
                        for j in range(columns.shape[1]):
                            
                            dpg.add_text(f"{columns.iloc[i,j]}")