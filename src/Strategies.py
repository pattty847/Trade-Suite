import time
import pandas_ta as ta
import pandas_market_calendars as mcal
import pandas as pd
import numpy as np
from datetime import datetime


def crossing(x, y):
    crossed = []
    for i in range(len(x)):
        # check if the value wt1 is greater than wt2 AND less than the previous row OR the opposite for crossing down
        if(x.iloc[i] > y.iloc[i] and x.iloc[i-1] < y.iloc[i-1]) | (x.iloc[i] < y.iloc[i] and x.iloc[i-1] > y.iloc[i-1]):
            crossed.append("True")
        else:
            crossed.append("False")
    return crossed


def wt():
    pass


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

    chlen = 9
    avg = 12
    malen = 3
    oslevel = -53
    oblevel = 53


    tfSrc = dataframe.copy(deep=True)

    tfSrc['HLC3'] = (tfSrc.iloc[:, 2] + tfSrc.iloc[:, 3] + tfSrc.iloc[:, 4]) / 3

    # ESA = Exponential Moving Average
    tfSrc['ESA'] = tfSrc['HLC3'].ewm(span=chlen, adjust=False).mean()

    # de = ema(abs(tfsrc - esa), chlen)
    tfSrc['DE'] = abs(tfSrc['HLC3'] - tfSrc['ESA']).ewm(span=chlen, adjust=False).mean()

    # ci = (tfsrc - esa) / (0.015 * de)
    tfSrc['CI'] = (tfSrc['HLC3'] - tfSrc['ESA']) / (0.015 * tfSrc['DE'])
    tfSrc['wt1'] = tfSrc['CI'].ewm(span=avg, adjust=False).mean()
    tfSrc['wt2'] = tfSrc['wt1'].rolling(malen).mean()
    tfSrc['wtVwap'] = tfSrc['wt1'] - tfSrc['wt2']
    tfSrc['wtOversold'] = tfSrc['wt2'] <= oslevel
    tfSrc['wtOverbought'] = tfSrc['wt2'] >= oblevel
    tfSrc['wtCross'] = crossing(tfSrc['wt1'], tfSrc['wt2'])

    # determines if the cross above is bullish by being <= 0
    tfSrc['wtCrossUp'] = tfSrc['wt2'] - tfSrc['wt1'] <= 0
    # determines if the cross above is bearish by being <= 0
    tfSrc['wtCrossDown'] = tfSrc['wt2'] - tfSrc['wt1'] >= 0

    # see crossing(x, y) function (passing the series shifted to determine if the last row was a cross)
    tfSrc['wtCrosslast'] = crossing(tfSrc['wt1'].shift(-1), tfSrc['wt2'].shift(-1))
    tfSrc['wtCrossUplast'] = tfSrc['wt2'].shift(-1) - tfSrc['wt1'].shift(-1) <= 0
    tfSrc['wtCrossDownlast'] = tfSrc['wt2'].shift(-1) - tfSrc['wt1'].shift(-1) >= 0

    # tfSrc['Symbol'] = symbol
    # tfSrc['Timeframe'] = timeframe

    # Buy signal.
    tfSrc['Buy'] = tfSrc['wtCross'] & tfSrc['wtCrossUp'] & tfSrc['wtOversold']

    # Sell signal
    tfSrc['Sell'] = tfSrc['wtCross'] & tfSrc['wtCrossDown'] & tfSrc['wtOverbought']

    tfSrc.drop(tfSrc.head(50).index, inplace=True)

    return (buys, sells)


def get_nyse_market_hours(market, start_date='2022-11-03', end_date='2023-01-01'):

    nyse = mcal.get_calendar('NYSE')
    nyse_schedule = pd.DataFrame(nyse.schedule(start_date, end_date))

    date = datetime.utcnow()
    
    # converting the current date
    # in datetime64 format
    date64 = np.datetime64(date)
    if market == "open":
        times_num64 = list(nyse_schedule.market_open.values)
    elif market == "close":
        times_num64 = list(nyse_schedule.market_close.values)

    timestamps = (times_num64 - date64) / np.timedelta64(1, 's')

    return list(map(lambda s: time.time() + s, timestamps))