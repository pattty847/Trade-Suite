import ccxt
import ccxt.binance as binance

for x in ccxt.exchanges:
	print(f"self.obj = {x}")