import json
import pandas as pd
import pandas_ta as pta
import numpy as np
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import schedule
import ccxt.pro as ccxtpro
import ccxt
from asyncio import run
from statsmodels.tsa.stattools import coint, adfuller
from screeninfo import get_monitors

def get_exchange_info(exchange_name):
    if exchange_name == "binance":
        return None
    
    exchange = getattr(ccxt, exchange_name)({'newUpdates': False})
    symbols = list(exchange.load_markets().keys())
    timeframes = list(exchange.describe().get('timeframes', None).keys())
    return {'symbols': symbols, 'timeframes': timeframes}


def primary_monitor():
    monitors = get_monitors()
    if len(monitors) == 1:
        # Only one monitor found, return its size
        main_monitor = monitors[0]
    else:
        # Multiple monitors found, find the primary one
        main_monitor = next(m for m in monitors if m.is_primary)
        
    return main_monitor


def draw_dpg_tools():
    with dpg.menu(label="DPG Tools"):
        dpg.add_menu_item(label="Show ImGui Demo", callback=dpg.show_imgui_demo)
        dpg.add_menu_item(label="Show ImPlot Demo", callback=dpg.show_implot_demo)
        dpg.add_menu_item(label="Show DPG Demo", callback=demo.show_demo)
        dpg.add_menu_item(label="Show Debug", callback=dpg.show_debug)
        dpg.add_menu_item(label="Show About", callback=lambda: dpg.show_tool(dpg.mvTool_About))
        dpg.add_menu_item(label="Show Metrics", callback=lambda: dpg.show_tool(dpg.mvTool_Metrics))
        dpg.add_menu_item(label="Show Documentation", callback=lambda: dpg.show_tool(dpg.mvTool_Doc))
        dpg.add_menu_item(label="Show Debug", callback=lambda: dpg.show_tool(dpg.mvTool_Debug))
        dpg.add_menu_item(label="Show Style Editor", callback=lambda: dpg.show_tool(dpg.mvTool_Style))
        dpg.add_menu_item(label="Show Font Manager", callback=lambda: dpg.show_tool(dpg.mvTool_Font))
        dpg.add_menu_item(label="Show Item Registry", callback=lambda: dpg.show_tool(dpg.mvTool_ItemRegistry))


def update_settings(settings, update):
    settings.update(update)
    with open("settings.json", "w") as jsonFile:
        json.dump(settings, jsonFile)

def get_time_in_past(days, month, year):
    """This function will be used to get a timestamp from days, month, years ago. 

    Args:
        days (int): days ago
        month (int): months ago
        year (int): years ago

    Returns:
        datetime in string format: %Y-%m-%dT%H:%M:%S - of time in past
    """
    import datetime
    year_ = str(year)
    y = int(f'20{year_[1:]}') # can't figure it out this will have to do until 2100 or I figure it out
    x = datetime.datetime(y, month, days)
    y2 = x.strftime("%Y-%m-%dT%H:%M:%S")
    return f"{y2}Z"


def zscore(series: pd.Series):
    """This will calculate the z-score of a series. 

    Args:
        series (pd.Series): Pandas series

    Returns:
        _type_: Z-Score series
    """
    return (series - series.mean()) / pta.stdev(series)


def help(message):
    last_item = dpg.last_item()
    group = dpg.add_group(horizontal=True)
    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))
    t = dpg.add_text("(?)", color=[0, 255, 0])
    with dpg.tooltip(t):
        dpg.add_text(message)
    

def _config(sender, keyword, user_data):

    widget_type = dpg.get_item_type(sender)
    items = user_data

    if widget_type == "mvAppItemType::mvRadioButton":
        value = True

    else:
        keyword = dpg.get_item_label(sender)
        value = dpg.get_value(sender)

    if isinstance(user_data, list):
        for item in items:
            dpg.configure_item(item, **{keyword: value})
    else:
        dpg.configure_item(items, **{keyword: value})


def _add_config_options(item, columns, *names, **kwargs):
        
    if columns == 1:
        if 'before' in kwargs:
            for name in names:
                dpg.add_checkbox(label=name, callback=_config, user_data=item, before=kwargs['before'], default_value=dpg.get_item_configuration(item)[name])
        else:
            for name in names:
                dpg.add_checkbox(label=name, callback=_config, user_data=item, default_value=dpg.get_item_configuration(item)[name])

    else:

        if 'before' in kwargs:
            dpg.push_container_stack(dpg.add_table(header_row=False, before=kwargs['before']))
        else:
            dpg.push_container_stack(dpg.add_table(header_row=False))

        for i in range(columns):
            dpg.add_table_column()

        for i in range(int(len(names)/columns)):

            with dpg.table_row():
                for j in range(columns):
                    dpg.add_checkbox(label=names[i*columns + j], 
                                        callback=_config, user_data=item, 
                                        default_value=dpg.get_item_configuration(item)[names[i*columns + j]])
        dpg.pop_container_stack()


def _log(sender, app_data, user_data):
    print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")


def searcher(searcher, result, search_list):
    """ This function is used to search a listbox based on a list.

    Args:
        searcher (dpg input item): this is the tag of the input box the user types into
        result (dpg listbox/combo box (maybe?)): this is the listbox tag 
        search_list (list): list of items you want to search
    """
    modified_list = []

    if dpg.get_value(searcher) == "*":
        modified_list.extend(iter(search_list))

    if dpg.get_value(searcher).lower():
        modified_list.extend(item for item in search_list if dpg.get_value(searcher).lower() in item.lower())

    dpg.configure_item(result, items=modified_list)


def _help(message):
    """ This function can be used to add an optional help popup that informs the user of something based on message.

    Args:
        message (_type_): _description_
    """
    last_item = dpg.last_item()
    group = dpg.add_group(horizontal=True)
    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))
    t = dpg.add_text("(?)", color=[0, 255, 0])
    with dpg.tooltip(t):
        dpg.add_text(message)


def sort_callback(sender, sort_specs):
    # TODO: Fix this function.
    """ This function will be called to sort a table's columns.

    Args:
        sender (_type_): _description_
        sort_specs (_type_): _description_

    Returns:
        _type_: _description_
    """

    # sort_specs scenarios:
    #   1. no sorting -> sort_specs == None
    #   2. single sorting -> sort_specs == [[column_id, direction]]
    #   3. multi sorting -> sort_specs == [[column_id, direction], [column_id, direction], ...]
    #
    # notes:
    #   1. direction is ascending if == 1
    #   2. direction is ascending if == -1

    # no sorting case
    if sort_specs is None: return

    rows = dpg.get_item_children(sender, 1)

    # create a list that can be sorted based on first cell
    # value, keeping track of row and value used to sort
    sortable_list = []
    for row in rows:
        first_cell = dpg.get_item_children(row, 1)[0]
        sortable_list.append([row, dpg.get_value(first_cell)])

    def _sorter(e):
        return e[1]

    sortable_list.sort(key=_sorter, reverse=sort_specs[0][1] < 0)

    # create list of just sorted row ids
    new_order = []
    for pair in sortable_list:
        new_order.append(pair[0])

    dpg.reorder_items(sender, 1, new_order)


def convert_timeframe(tf):
    """This function is used when you need to convert a timeframe (1h, 1d, etc) into the dearpygui equivalent

    Args:
        tf (String): The timeframe you want to convert to dearpygui format

    Returns:
        int: dearpygui time unit
    """
    if tf[len(tf) - 1] == 's':
        return dpg.mvTimeUnit_S
    elif tf[len(tf) - 1] == 'm':
        return dpg.mvTimeUnit_Min
    elif tf[len(tf) - 1] == 'h':
        return dpg.mvTimeUnit_Hr
    elif tf[len(tf) - 1] == 'd':
        return dpg.mvTimeUnit_Day
    elif tf[len(tf) - 1] == 'M':
        return dpg.mvTimeUnit_Mo



def candles_to_list( candles):
    """This function will convert a dataframe object containing OHLCV data into list format

    Args:
        candles (DataFrame): candlestick data (OHLCV)

    Returns:
        tuple: columns from dataframe returned as tuple containing lists
    """
    dates = list(candles['date']/1000)
    opens = list(candles['open'])
    closes = list(candles['close'])
    lows = list(candles['low'])
    highs = list(candles['high'])
    volume = list(candles['volume'])
    return (dates, opens, closes, lows, highs, volume)



def push_to_schedule(func, delay, timeframe):
    if timeframe == "seconds":
        schedule.every(delay).seconds.do(func)
    elif timeframe == "minutes":
        schedule.every(delay).minutes.do(func)
    elif timeframe == "hours":
        schedule.every(delay).hours.do(func)
    elif timeframe == "days":
        schedule.every(delay).days.do(func)
    elif timeframe == "weeks":
        schedule.every(delay).weeks.do(func)

def run_pending(self):
    while True:
        schedule.run_pending()



def find_cointegrated_pairs( data: pd.DataFrame, pvalue_filter: float):
    """This is a function which you want to use to draw a heatmap of cointegrated values between them. It will return what you need for a heatmap series in "pvalue_matrix" var.

    Args:
        data (pd.DataFrame): This is a matrix of closes
        pvalue_filter (float): Pvalues less than pvalue_filter

    Returns:
        _type_: tuple containing the cointegration scores, pvalues, and pairs thare are under a certain pvalue.
    """
    n = data.shape[1]
    score_matrix = np.zeros((n, n))
    pvalue_matrix = np.ones((n, n))
    keys = data.keys()
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            S1 = data[keys[i]]
            S2 = data[keys[j]]
            result = coint(S1, S2)
            score = result[0]
            pvalue = result[1]
            score_matrix[i, j] = score
            pvalue_matrix[i, j] = pvalue
            if pvalue < pvalue_filter:
                pairs.append((keys[i], keys[j]))
    return (score_matrix, pvalue_matrix, pairs)



def first_time_back():
    """TODO: First Time Back (FTB) to the Supply or Demand zone
    """
    pass



def hex_to_RGB(hex):
    ''' "#FFFFFF" -> [255,255,255] '''
    # Pass 16 to the integer function for change of base
    return [int(hex[i:i+2], 16) for i in range(1,6,2)]


def RGB_to_hex(RGB):
    ''' [255,255,255] -> "#FFFFFF" '''
    # Components need to be integers for hex to make sense
    RGB = [int(x) for x in RGB]
    return "#"+"".join(["0{0:x}".format(v) if v < 16 else
                "{0:x}".format(v) for v in RGB])


def candles_to_list( candles):
    """This function will convert a dataframe object containing OHLCV data into list format

    Args:
        candles (DataFrame): candlestick data (OHLCV)

    Returns:
        tuple: columns from dataframe returned as tuple containing lists
    """
    dates = list(candles['date']/1000)
    opens = list(candles['open'])
    closes = list(candles['close'])
    lows = list(candles['low'])
    highs = list(candles['high'])
    volume = list(candles['volume'])
    return (dates, opens, closes, lows, highs, volume)