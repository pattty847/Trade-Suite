import asyncio
import Exchanges.FTX as FTX

data = asyncio.run(FTX.fetch_candles("BTC-PERP", "300"))
print(data["time"])