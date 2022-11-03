import pandas_ta as ta
import pandas_market_calendars as mcal
import pandas as pd


def wavetrend(dataframe):
    """ This function takes a dataframe of dates, OHLCV and returns a tuple of buys and sells contained in lists as ordered pairs. 
    Mostly going to be used for annotating charts.

    Args:
        dataframe (_type_): _description_

    Returns:
        tuple: Tuple containing two lists, buys and sells, which contain ordered pairs of a date and price value for annotations. 
    """

    buys = []
    sells = []

    return (buys, sells)


def get_nyse_market_hours(start_date='2022-11-03', end_date='2023-01-01'):

    nyse = mcal.get_calendar('NYSE')
    nyse_schedule = pd.DataFrame(nyse.schedule(start_date, end_date), dtype='str')

    return nyse_schedule

print(get_nyse_market_hours().market_open)