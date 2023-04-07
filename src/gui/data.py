import json
import os
import ccxt.async_support as ccxt
import pandas as pd
import logging
import asyncio
from typing import List

class DataCollector:
    def __init__(self, exchanges, symbols, timeframe):
        self.exchanges = exchanges
        self.symbols = symbols
        self.timeframe = timeframe
        self.logger = logging.getLogger(__name__)

    def set_exchanges(self, exchanges):
        """
        The set_exchanges function changes the exchanges that are used in the strategy.
                
        
        :param self: Represent the instance of the class
        :param exchanges: Set the exchanges that are used in the backtest
        :return: The value of self
        :doc-author: Trelent
        """
        self.logger.info(f"Changing exchanges from {self.exchanges} to {exchanges}.")
        self.exchanges = exchanges
    
    def set_symbols(self, symbols):
        """
        The set_symbols function changes the symbols that are being traded.
                
        
        :param self: Represent the instance of the class
        :param symbols: Change the symbols that are being used in the trading strategy
        :return: Nothing
        :doc-author: Trelent
        """
        self.logger.info(f"Changing symbols from {self.symbols} to {symbols}.")
        self.symbols = symbols
        
    def save_candles_to_file(self, exchange, symbol, timeframe, candles: pd.DataFrame):
        """
        The save_candles_to_file function saves the candles to a file.
        
        :param self: Represent the instance of the class
        :param exchange: Create the directory in which the data will be saved
        :param symbol: Create the file name
        :param timeframe: Determine the timeframe of the candle data
        :param candles: pd.DataFrame: Pass a dataframe to the function
        :return: A csv file of the candles dataframe
        :doc-author: Trelent
        """
        symbol = symbol.replace("/", "_")
        directory = f"data/exchange/{exchange}"
        os.makedirs(directory, exist_ok=True)
        self.logger.info(f"Saving {symbol}_{timeframe}...")
        candles.to_csv(f"{directory}/{symbol}_{timeframe}.csv", index=True)

    def load_candles_from_file(self, exchange, symbol, timeframe):
        """
        The load_candles_from_file function is used to load the candles from a file.
            If the file exists, it will be loaded into a pandas dataframe and returned.
            If not, an empty dataframe with columns specified by self.indicators will be created and returned.
        
        :param self: Bind the method to the object
        :param exchange: Specify which exchange the data is being pulled from
        :param symbol: Specify the symbol you want to get data for
        :param timeframe: Determine the timeframe of the candles being loaded
        :return: A dataframe
        :doc-author: Trelent
        """
        filename = (
            f"data/exchange/{exchange}/{symbol.replace('/', '_')}_{timeframe}.csv"
        )
        if os.path.exists(filename):
            self.logger.info(f"Loaded: {exchange.upper()}:{symbol.replace('/', '_')}_{timeframe} from file.")
            df = pd.read_csv(filename)
            df['dates'] = pd.to_datetime(df['dates'])
            return df
        else:
            # TODO: Make columns use self.indicators to apply the users specified TA features or use this as default
            columns = ["dates", "opens", "highs", "lows", "closes", "volumes", "sma_5", "sma_20", "ema_12", "ema_26", "macd", "rsi"]
            return pd.DataFrame(columns=columns)
    
    async def fetch_candles_(self, exchange, symbol, timeframe, since, limit, dataframe, max_retries):
        """
        This asynchronous function fetches historical OHLCV (Open, High, Low, Close, Volume) candlestick data from 
        multiple cryptocurrency exchanges for specified symbols and timeframes. The data can be returned as a pandas 
        DataFrame or a dictionary. The function also supports retries in case of errors during data fetching. Technical
        indicators like RSI, MACD, MOM, etc are also calculaated and returned.

        Arguments:
            exchanges (List[str]): List of exchange names as strings.
            symbols (List[str]): List of asset symbols as strings (e.g. 'BTC/USD').
            timeframe (str): Timeframe of the candles (e.g. '1m', '1h', '1d').
            since (str): ISO8601 formatted string representing the starting date for fetching candles.
            limit (int): Maximum number of candles to fetch in one request.
            dataframe (bool): Whether to return the data as a pandas DataFrame (True) or as a dictionary (False).
            max_retries (int, optional): Maximum number of retries in case of errors during data fetching. Defaults to 3.

        Returns:
            dict or pd.DataFrame: A dictionary or pandas DataFrame containing the historical OHLCV data, grouped by exchange and symbol.

        Example usage:
            data = await fetch_candles(
                exchanges=['binance', 'coinbase'],
                symbols=['BTC/USD', 'ETH/USD'],
                timeframe='1h',
                since='2021-01-01T00:00:00Z',
                limit=100,
                dataframe=True
            )
        """
        api = getattr(ccxt, exchange)()
        if not api.has['fetchOHLCV']:
            self.logger.info(f"{exchange.upper()} does not have fetch OHLCV.")
            return None

        # Load cached candle history which includes TA indicators
        candles = self.load_candles_from_file(exchange, symbol, timeframe)
        new_candles = []

        timeframe_duration_in_seconds = api.parse_timeframe(timeframe)
        timedelta = limit * timeframe_duration_in_seconds * 1000
        now = api.milliseconds()
        fetch_since = (
            api.parse8601(since)
            if candles.empty
            else int(candles['dates'].iloc[-1].timestamp() * 1000)
        )

        # Fetch candles
        while True:
            new_candle_batch = None
            for num_retries in range(max_retries):
                try:
                    new_candle_batch = await api.fetch_ohlcv(
                        symbol, timeframe, since=fetch_since, limit=limit
                    )
                except ccxt.ExchangeError as e:
                    print(e)
                    await asyncio.sleep(1)
                if new_candle_batch is not None:
                    break
            if new_candle_batch is None:
                await api.close()
                return None

            new_candles += new_candle_batch

            if len(new_candle_batch):
                last_time = new_candle_batch[-1][0] + timeframe_duration_in_seconds * 1000
                print(len(new_candle_batch), "candles from", api.iso8601(new_candle_batch[0][0]), "to", api.iso8601(new_candle_batch[-1][0]))
            else:
                last_time = fetch_since + timedelta
                self.logger.info("no candles")

            if last_time >= now:
                break

            fetch_since = last_time

        # Combine old and new candles
        if not candles.empty:
            candles = candles.iloc[:-1]

        # This dataframe's dates will contain timestamps in ms from the exchange
        new_candles_df = pd.DataFrame(new_candles, columns=["dates", "opens", "highs", "lows", "closes", "volumes"])
        new_candles_df["dates"] = pd.to_datetime(new_candles_df['dates'], unit='ms')
        candles = pd.concat([candles, new_candles_df]).reset_index(drop=True)

        # Calculate technical indicators
        updated_candles = self.calculate_ta(candles)

        # Clean the data
        # updated_candles = self.clean(updated_candles)

        # Save candles with technical indicators
        self.save_candles_to_file(exchange, symbol, timeframe, updated_candles)

        await api.close()
        
        return (exchange, symbol, updated_candles)
    
    def calculate_ta(self, data):
        """
        The calculate_ta function adds technical analysis indicators to the dataframe.
            The function takes in a dataframe and returns a new dataframe with the following columns:
                - sma_5: Simple Moving Average of 5 periods.
                - sma_20: Simple Moving Average of 20 periods.
                - ema_12: Exponential Moving Average of 12 periods. 
                - ema_26: Exponential Moving Average of 26 periods. 
                - macd = (ema12-ema26).round(3) : MACD indicator, which is calculated by subtracting EMA26 from EMA
        
        :param self: Represent the instance of the class
        :param data: Pass the dataframe to the function
        :return: A dataframe with technical indicators added
        :doc-author: Trelent
        """
        self.logger.info(f"Adding technical analysis indicators.")
        data.set_index('dates', inplace=True)

        # create technical indicators
        data['sma_5'] = data['closes'].rolling(window=5).mean().round(3)
        data['sma_20'] = data['closes'].rolling(window=20).mean().round(3)
        data['ema_12'] = data['closes'].ewm(span=12, adjust=False).mean().round(3)
        data['ema_26'] = data['closes'].ewm(span=26, adjust=False).mean().round(3)
        data['macd'] = (data['ema_12'] - data['ema_26']).round(3)
        data['rsi'] = ta.rsi(data['closes'], timeperiod=14).round(3)
        data['bb_upper'], data['bb_middle'], data['bb_lower'] = ta.BBANDS(data['closes'], timeperiod=20)
        data['stoch_k'], data['stoch_d'] = ta.STOCH(data['highs'], data['lows'], data['closes'], fastk_period=14, slowk_period=3, slowd_period=3)

        return data

    async def fetch_candles(self, exchanges: List[str], symbols: List[str], timeframe: str, since: str, limit: int, dataframe: bool, max_retries=3):
        """
        The fetch_candles function fetches candles for a list of symbols from a list of exchanges.
        
        :param self: Represent the instance of the class
        :param exchanges: List[str]: Specify which exchanges to fetch data from
        :param symbols: List[str]: Specify the symbols for which you want to fetch candles
        :param timeframe: str: Specify the timeframe of the candles
        :param since: str: Specify the start date of the candles
        :param limit: int: Limit the amount of candles that are returned
        :param dataframe: bool: Determine whether the data should be returned in a pandas dataframe or not
        :param max_retries: Limit the number of times a request is retried if it fails
        :return: A dictionary of candles
        :doc-author: Trelent

        Example:
            exchanges = ['coinbasepro']
            symbols = ['BTC/USD', "ETH/USD", "LTC/USD"]
            timeframe = '1h'
            collector = DataCollector(exchanges, symbols, timeframe)

            loop = asyncio.get_event_loop()
            data = loop.run_until_complete(collector.fetch_candles(exchanges, symbols, timeframe, "2023-03-20 00:00:00", 1000, True))

            chart.plot(data['coinbasepro']['BTC/USD'])
        """
        tasks = [
            self.fetch_candles_(exchange, symbol, timeframe, since, limit, dataframe, max_retries)
            for exchange in exchanges
            for symbol in symbols
        ]
        results = await asyncio.gather(*tasks)
        candles = {}
        for exchange, symbol, result in results:
            if exchange not in candles:
                candles[exchange] = {}
            candles[exchange][symbol] = result

        return candles

# FETCH CANDLES CODE EXAMPLE:
# exchanges = ['coinbasepro']
# symbols = ['BTC/USD', "ETH/USD", "LTC/USD"]
# timeframe = '1h'
# collector = DataCollector(exchanges, symbols, timeframe)

# loop = asyncio.get_event_loop()
# data = loop.run_until_complete(collector.fetch_candles(exchanges, symbols, timeframe, "2023-03-20 00:00:00", 1000, True))

# chart.plot(data['coinbasepro']['BTC/USD'])

    async def fetch_percentage_change_vs_btc(self, exchange, symbols, timeframe, lookback_minutes, max_retries):
        """
        The fetch_percentage_change_vs_btc function fetches the percentage change of a symbol vs. BTC for a given timeframe and lookback period.
        
        :param self: Bind the method to an object
        :param exchange: Determine which exchange to use
        :param symbols: Specify which symbols to fetch data for
        :param timeframe: Specify the timeframe of the data that is returned
        :param lookback_minutes: Determine how far back in time to look for the percentage change
        :param max_retries: Determine how many times the function will try to retrieve data from an exchange before giving up
        :return: A list of dictionaries
        :doc-author: Trelent
        """
        
        async with getattr(ccxt, exchange)() as api:
            available_symbols = set((await api.load_markets()).keys())
            tasks = [self.fetch_percentage_change_vs_btc_(exchange, symbol, timeframe, lookback_minutes, max_retries) for symbol in symbols if symbol in available_symbols]
            results = await asyncio.gather(*tasks)
            return results
        
    # FETCH CANDLES - RETURN PERCENTAGE GAINS
    async def fetch_percentage_change_vs_btc_(self, exchange, symbol, timeframe, lookback_minutes, max_retries):
        api = getattr(ccxt, exchange)()
        
        if not api.has['fetchOHLCV']:
            self.logger.info(f"{exchange.upper()} does not have fetch OHLCV.")
            return None

        timeframe_duration_in_seconds = api.parse_timeframe(timeframe)
        lookback_milliseconds = lookback_minutes * 60 * 1000
        now = api.milliseconds()
        since = now - (lookback_milliseconds + timeframe_duration_in_seconds * 1000)  # Add an extra candle duration

        current_candle = None
        past_candle = None
        for num_retries in range(max_retries):
            try:
                current_candle = await api.fetch_ohlcv(symbol, timeframe, limit=1)
                past_candle = await api.fetch_ohlcv(symbol, timeframe, since=since, limit=2)
            except ccxt.ExchangeError as e:
                print(e)
                await asyncio.sleep(1)
            if current_candle is not None and past_candle is not None:
                break

        if current_candle is None or past_candle is None:
            await api.close()
            return None

        current_candle_df = pd.DataFrame(current_candle, columns=["dates", "opens", "highs", "lows", "closes", "volumes"])
        current_candle_df["dates"] = pd.to_datetime(current_candle_df['dates'], unit='ms')

        past_candle_df = pd.DataFrame(past_candle, columns=["dates", "opens", "highs", "lows", "closes", "volumes"])
        past_candle_df["dates"] = pd.to_datetime(past_candle_df['dates'], unit='ms')

        print(current_candle_df.to_string(index=False))
        print(past_candle_df.to_string(index=False))

        await api.close()

        return (exchange, symbol, past_candle_df.iloc[-1:], current_candle_df)  # Return only the last past candle
        
    def percentage_gains(self, latest_data):
        """
        The percentage_gains function takes in a list of tuples, where each tuple contains the following:
            1. The exchange name (e.g., 'binance')
            2. The symbol (e.g., 'BTC/USDT')
            3. A pandas DataFrame containing the past data for that symbol on that exchange, with columns ['closes', 'opens'] and an index of timestamps from oldest to newest
            4. A pandas DataFrame containing the current data for that symbol on that exchange, with columns ['closes', 'opens'] and an index of timestamps from oldest to
        
        :param self: Represent the instance of the class
        :param latest_data: Pass the data from the get_latest_data function to this function
        :return: A dict of the percentage gains for each asset
        :doc-author: Trelent
        """
        btc_past_price = None
        btc_current_price = None
        percentage_gains = {}
        for data in latest_data:
            if not data:
                continue
            symbol = data[1]

            past_close_price = data[2]['closes'].iloc[0]
            current_close_price = data[3]['closes'].iloc[0]

            if symbol == 'BTC/USDT':
                btc_past_price = past_close_price
                btc_current_price = current_close_price
            else:
                asset_percentage_gain = (current_close_price / past_close_price - 1) * 100
                btc_percentage_gain = (btc_current_price / btc_past_price - 1) * 100
                relative_percentage_gain = asset_percentage_gain - btc_percentage_gain

                percentage_gains[symbol] = relative_percentage_gain
        return percentage_gains
    
    def current_daily_volume(self, exchanges, symbols):
        daily_volume = {}
        


# # Replace 'binance' with the desired exchange, and add the symbols you want to track, including BTC
# exchange = 'coinbasepro'
# symbols = ['BTC/USDT', 'ETH/USDT', 'AAVE/USDT', 'ACH/USD', 'ATOM/USD', 'DOGE/USD']
# timeframe = '1h'
# lookback_minutes = 1000
# max_retries = 3
# collector = DataCollector(exchange, symbols, timeframe)

# latest_data = asyncio.run(collector.fetch_percentage_change_vs_btc(exchange, symbols, timeframe, lookback_minutes, max_retries))

# percentage_gains = collector.percentage_gains(latest_data)

       
# print(percentage_gains)