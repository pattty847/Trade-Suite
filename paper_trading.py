import ccxt.pro as ccxtpro
import ccxt
import asyncio
import logging
import argparse
import numpy as np

"""
    This file is a testing playground: Aggregating many exchange's trade data into one + cummulative volume delta and a paper trading class.
"""

logging.basicConfig(
        level=logging.INFO, 
        filename="trade_logs.log", 
        filemode="a", 
        format='%(asctime)s - %(message)s', 
        datefmt='%d-%b-%y %H:%M:%S'
    )

class PaperTrading:

    def __init__(self, symbol, initial_balance=1000, window_size=20, num_std=2, max_positions=5):
        self.symbol = symbol
        self.initial_balance = initial_balance
        self.window_size = window_size
        self.num_std = num_std
        self.max_positions = max_positions
        self.balance = initial_balance
        self.profit = self.balance - initial_balance
        self.positions = []
        self.trades = []

    def bb(self, trades):
        for trade in trades:
            self.trades.append(trade)

        prices = [t['price'] for t in self.trades[-self.window_size:]]

        if len(prices) < self.window_size:
            return
        middle_band = np.mean(prices)
        std = np.std(prices)
        upper_band = middle_band + self.num_std * std
        lower_band = middle_band - self.num_std * std

        # check if we should buy
        if len(self.positions) < self.max_positions and trade['price'] < lower_band:
            amount = min(0.1 * self.balance / trade['price'], self.max_positions - len(self.positions))
            cost = amount * trade['price']
            self.balance -= cost
            self.positions.append({'symbol': trade['symbol'], 'amount': amount, 'price': trade['price'], 'timestamp': trade['timestamp']})
            self.trades.append(trade)
            print(f"Bought {amount} {trade['symbol']} at {trade['price']} - Balance: {self.balance}")

        # check if we should sell
        elif len(self.positions) > 0 and trade['price'] > upper_band:
            position = self.positions.pop(0)
            cost = position['amount'] * trade['price']
            self.balance += cost
            self.trades.append(trade)
            print(f"Sold {position['amount']} {position['symbol']} at {trade['price']} - Balance: {self.balance} - Profit: {self.profit}")



class TradeWatch(PaperTrading):

    def __init__(self) -> None:
        self.cvd = 0

    async def fetch(self, exchange_name, symbol):
        exchange_class = getattr(ccxtpro, exchange_name)
        exchange = exchange_class(
            {
                "enableRateLimit": True,  # add rate limiter
                "newUpdates": True
            }
        )
        logging.info(f'Starting {symbol} {exchange}...')

        while True:
            try:
                # watch the data using the specified method
                trades = await getattr(exchange, "watchTrades")(symbol)
                pt.bb(trades)
                if trades:
                    for trade in trades:
                        self.cvd += trade['cost'] if trade['side'] == "buy" else -trade['cost']
                        logging.info({
                            'exchange': exchange_name,
                            'symbol': trade['symbol'],
                            'side': trade['side'],
                            'price': trade['price'],
                            'amount': trade['amount'],
                            'cost': trade['cost'],
                            'cvd': self.cvd,
                            'id': trade['id'],
                            'timestamp': trade['timestamp'],
                        })

            except ccxt.BaseError as e:
                logging.info(e)
                logging.info(f"{exchange_name} closed.")
                await exchange.close()
                break

            except KeyboardInterrupt:
                logging.info(f"Closing {exchange_name}")
                await exchange.close()

    async def fetch_all(self, exchange_names, symbol):
        tasks = []
        for exchange_name in exchange_names:
            tasks.append(self.fetch(exchange_name, symbol))
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    pt = PaperTrading("BTC/USDT")
    tw = TradeWatch()
    logging.info("Starting program...")

    # Create the parser
    parser = argparse.ArgumentParser(description='Command Line Control System')

    # Add the arguments
    parser.add_argument('-a', '--action', choices=['trades'], required=True, help='Action to perform.')
    parser.add_argument('-e', '--exchange', nargs='+', required=True, help='Exchange(s) to watch.')
    parser.add_argument('-s', '--symbol', required=False, help="What symbol's trade to watch. (default BTC/USDT)")

    # Parse the arguments
    args = parser.parse_args()

    # Perform the action
    if args.action == 'trades':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            tw.fetch_all(
                exchange_names=['coinbasepro', 'okx', 'kucoin', 'bybit', 'huobi', 'bitfinex', 'cryptocom', 'binanceus', 'kraken'] if 'top' in args.exchange else args.exchange, 
                symbol=args.symbol if args.symbol else "BTC/USDT"
                )
            )