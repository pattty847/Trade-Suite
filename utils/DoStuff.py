import json
import pandas as pd
import pandas_ta as pta
import numpy as np
import dearpygui.dearpygui as dpg

def update_settings(settings, update):

    settings.update(update)
    with open("settings.json", "w") as jsonFile:
        json.dump(settings, jsonFile)

def get_time_in_past( days, month, year):
        """This function will be used to get a timestamp from days, month, years ago. 

        Args:
            days (_type_): _description_
            month (_type_): _description_
            year (_type_): _description_

        Returns:
            _type_: _description_
        """
        import datetime
        year_ = str(year)
        y = int(f'20{year_[1:]}') # can't figure it out this will have to do until 2100 or I figure it out
        x = datetime.datetime(y, month, days)
        y2 = x.strftime("%Y-%m-%dT%H:%M:%S")
        return f"{y2}Z"


def zscore( series: pd.Series):
    """This will calculate the z-score of a series. 

    Args:
        series (pd.Series): Pandas series

    Returns:
        _type_: Z-Score series
    """
    return (series - series.mean()) / pta.stdev(series)



def convert_timeframe( tf):
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



def find_cointegrated_pairs( data: pd.DataFrame, pvalue_filter: float):
    """This is a function which you want to use to draw a heatmap of cointegrated values between them. It will return what you need for a heatmap series in "pvalue_matrix" var.

    Args:
        data (pd.DataFrame): This is a matrix of closes
        pvalue_filter (float): This is the value you want to filter pvalues which are less than

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



def first_time_back(self):
    """TODO: First Time Back (FTB) to the Supply or Demand zone
    """
    pass



def hex_to_RGB( hex):
    ''' "#FFFFFF" -> [255,255,255] '''
    # Pass 16 to the integer function for change of base
    return [int(hex[i:i+2], 16) for i in range(1,6,2)]


def RGB_to_hex( RGB):
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