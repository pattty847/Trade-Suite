import json


def update_settings(settings, update):

    settings.update(update)
    with open("settings.json", "w") as jsonFile:
        json.dump(settings, jsonFile)


def candles_to_list(self, candles):
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