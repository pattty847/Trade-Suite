import json
import pandas as pd
import ccxt.pro as ccxtpro
import asyncio
from statsmodels.tsa.arima.model import ARIMA

class PaperTradingAccount:
    def __init__(self, initial_balance, trade_fee_pct, ohlcv_file):
        self.balance = initial_balance
        self.trade_fee_pct = trade_fee_pct
        self.historical_data = self.load_ohlcv_data(ohlcv_file)
        self.trade_cache = []
        self.profits = []
        self.open_positions = {}  # Initialize the open_positions dictionary

    def add_trade_data(self, trade_data):
        self.trade_cache.append(trade_data)

    def clear_trade_cache(self):
        self.trade_cache = []

    def go_long(self, symbol, price, size):
        position_cost = price * size
        fee = position_cost * self.trade_fee_pct

        if self.balance - position_cost - fee >= 0:
            self.balance -= position_cost + fee
            self.open_positions[symbol] = {"type": "long", "price": price, "size": size}
            print(f"Long position opened for {symbol} at {price} with size {size}")
        else:
            print("Not enough balance to go long")

    def go_short(self, symbol, price, size):
        position_cost = price * size
        fee = position_cost * self.trade_fee_pct

        if self.balance - position_cost - fee >= 0:
            self.balance -= position_cost + fee
            self.open_positions[symbol] = {"type": "short", "price": price, "size": size}
            print(f"Short position opened for {symbol} at {price} with size {size}")
        else:
            print("Not enough balance to go short")

    def close_position(self, symbol, current_price):
        position = self.open_positions.get(symbol)

        if position:
            position_type = position["type"]
            price = position["price"]
            size = position["size"]

            if position_type == "long":
                profit = (current_price - price) * size
            elif position_type == "short":
                profit = (price - current_price) * size

            fee = abs(profit) * self.trade_fee_pct
            self.balance += profit - fee
            self.profits.append(profit)

            del self.open_positions[symbol]
            print(f"{position_type.capitalize()} position closed for {symbol} at {current_price}. Profit: {profit - fee}")
        else:
            print(f"No open position for {symbol}")

    def load_ohlcv_data(self, ohlcv_file):
        with open(ohlcv_file, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)

        # Create a DateTimeIndex with a fixed frequency
        df['dates'] = pd.to_datetime(df['dates'], unit='s')
        dt_index = pd.DatetimeIndex(df['dates'], freq='T')

        # Replace the date index with the new DateTimeIndex
        df.set_index(dt_index, inplace=True)
        df.drop(columns='dates', inplace=True)

        return df

    def arima_trade_decision(self):
        # Train ARIMA model on historical data
        model = ARIMA(self.historical_data['closes'], order=(5, 1, 0))
        model_fit = model.fit()

        # Predict the next price based on real-time trade data
        trade_prices = [trade['price'] for trade in self.trade_cache]
        trade_series = pd.Series(trade_prices, name='closes')
        exog_data = pd.concat([self.historical_data[['closes']].iloc[-1:], trade_series], ignore_index=True).iloc[1:]
        forecast = model_fit.predict(start=len(self.historical_data), end=len(self.historical_data), exog=exog_data)

        # Make a trading decision based on the forecast
        current_price = trade_prices[-1]
        predicted_price = forecast.iloc[-1]

        if predicted_price > current_price:
            # Go long
            return 'long'
        else:
            # Go short
            return 'short'
        
    async def start_websocket(self, exchange_name, symbol, limit):
        exchange_class = getattr(ccxtpro, exchange_name)
        exchange = exchange_class(
            {
                "enableRateLimit": True,  # add rate limiter
                "newUpdates": True
            }
        )

        while True:
            try:
                # watch the data using the specified method
                orderbook = await getattr(exchange, "watchOrderBook")(symbol, limit)
                trades = await getattr(exchange, "watchTrades")(symbol)

                if orderbook['bids'] and orderbook['asks']:
                    #print(trades)
                    #print(orderbook['bids'][0], orderbook['asks'][0])

                    # Update trade cache
                    for trade in trades:
                        self.add_trade_data(trade)

                    # Make a trading decision based on the ARIMA model
                    decision = self.arima_trade_decision()

                    # Execute the trading decision
                    if decision == 'long':
                        # Go long at the best ask price
                        self.go_long(symbol, orderbook['asks'][0][0], self.balance * 0.1)
                    elif decision == 'short':
                        # Go short at the best bid price
                        self.go_short(symbol, orderbook['bids'][0][0], self.balance * 0.1)

            except KeyboardInterrupt:
                print("KeyboardInterrupt detected. Closing exchange...")
                await exchange.close()
                break

        print("Exchange closed.")

async def main():
    account = PaperTradingAccount(initial_balance=100000, trade_fee_pct=0.01, ohlcv_file='/home/pepe/Desktop/Programming/Python/Trade-Suite/exchanges/candles/coinbasepro/BTC_USD_1m.json')
    await account.start_websocket(exchange_name='coinbasepro', symbol='BTC/USD', limit=10)

if __name__ == "__main__":
    asyncio.run(main())