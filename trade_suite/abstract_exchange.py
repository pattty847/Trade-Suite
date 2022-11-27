from typing import Type
import ccxt.aax as aax
import ccxt.alpaca as alpaca
import ccxt.ascendex as ascendex
import ccxt.bequant as bequant
import ccxt.bibox as bibox
import ccxt.bigone as bigone
import ccxt.binance as binance
import ccxt.binancecoinm as binancecoinm
import ccxt.binanceus as binanceus
import ccxt.binanceusdm as binanceusdm
import ccxt.bit2c as bit2c
import ccxt.bitbank as bitbank
import ccxt.bitbay as bitbay
import ccxt.bitbns as bitbns
import ccxt.bitcoincom as bitcoincom
import ccxt.bitfinex as bitfinex
import ccxt.bitfinex2 as bitfinex2
import ccxt.bitflyer as bitflyer
import ccxt.bitforex as bitforex
import ccxt.bitget as bitget
import ccxt.bithumb as bithumb
import ccxt.bitmart as bitmart
import ccxt.bitmex as bitmex
import ccxt.bitopro as bitopro
import ccxt.bitpanda as bitpanda
import ccxt.bitrue as bitrue
import ccxt.bitso as bitso
import ccxt.bitstamp as bitstamp
import ccxt.bitstamp1 as bitstamp1
import ccxt.bittrex as bittrex
import ccxt.bitvavo as bitvavo
import ccxt.bkex as bkex
import ccxt.bl3p as bl3p
import ccxt.blockchaincom as blockchaincom
import ccxt.btcalpha as btcalpha
import ccxt.btcbox as btcbox
import ccxt.btcex as btcex
import ccxt.btcmarkets as btcmarkets
import ccxt.btctradeua as btctradeua
import ccxt.btcturk as btcturk
import ccxt.buda as buda
import ccxt.bw as bw
import ccxt.bybit as bybit
import ccxt.bytetrade as bytetrade
import ccxt.cex as cex
import ccxt.coinbase as coinbase
import ccxt.coinbaseprime as coinbaseprime
import ccxt.coinbasepro as coinbasepro
import ccxt.coincheck as coincheck
import ccxt.coinex as coinex
import ccxt.coinfalcon as coinfalcon
import ccxt.coinmate as coinmate
import ccxt.coinone as coinone
import ccxt.coinspot as coinspot
import ccxt.crex24 as crex24
import ccxt.cryptocom as cryptocom
import ccxt.currencycom as currencycom
import ccxt.delta as delta
import ccxt.deribit as deribit
import ccxt.digifinex as digifinex
import ccxt.exmo as exmo
import ccxt.flowbtc as flowbtc
import ccxt.fmfwio as fmfwio
import ccxt.ftx as ftx
import ccxt.ftxus as ftxus
import ccxt.gate as gate
import ccxt.gateio as gateio
import ccxt.gemini as gemini
import ccxt.hitbtc as hitbtc
import ccxt.hitbtc3 as hitbtc3
import ccxt.hollaex as hollaex
import ccxt.huobi as huobi
import ccxt.huobijp as huobijp
import ccxt.huobipro as huobipro
import ccxt.idex as idex
import ccxt.independentreserve as independentreserve
import ccxt.indodax as indodax
import ccxt.itbit as itbit
import ccxt.kraken as kraken
import ccxt.kucoin as kucoin
import ccxt.kucoinfutures as kucoinfutures
import ccxt.kuna as kuna
import ccxt.latoken as latoken
import ccxt.lbank as lbank
import ccxt.lbank2 as lbank2
import ccxt.liquid as liquid
import ccxt.luno as luno
import ccxt.lykke as lykke
import ccxt.mercado as mercado
import ccxt.mexc as mexc
import ccxt.mexc3 as mexc3
import ccxt.ndax as ndax
import ccxt.novadax as novadax
import ccxt.oceanex as oceanex
import ccxt.okcoin as okcoin
import ccxt.okex as okex
import ccxt.okex5 as okex5
import ccxt.okx as okx
import ccxt.paymium as paymium
import ccxt.phemex as phemex
import ccxt.poloniex as poloniex
import ccxt.probit as probit
import ccxt.qtrade as qtrade
import ccxt.ripio as ripio
import ccxt.stex as stex
import ccxt.therock as therock
import ccxt.tidebit as tidebit
import ccxt.tidex as tidex
import ccxt.timex as timex
import ccxt.tokocrypto as tokocrypto
import ccxt.upbit as upbit
import ccxt.wavesexchange as wavesexchange
import ccxt.wazirx as wazirx
import ccxt.whitebit as whitebit
import ccxt.woo as woo
import ccxt.yobit as yobit
import ccxt.zaif as zaif
import ccxt.zb as zb
import ccxt.zipmex as zipmex
import ccxt.zonda as zonda
from dataclasses import dataclass
import ccxtpro


@dataclass
class MarketValue:
  param1: int
  param2: float
  param3: str

# class for public usage in the rest of your program
class AbstractedMarket:
    def __init__(self, name: str): # simple input value how to interact with it
        self.obj = aax
        self.obj = alpaca
        self.obj = ascendex
        self.obj = bequant
        self.obj = bibox
        self.obj = bigone
        self.obj = binance
        self.obj = binancecoinm
        self.obj = binanceus
        self.obj = binanceusdm
        self.obj = bit2c
        self.obj = bitbank
        self.obj = bitbay
        self.obj = bitbns
        self.obj = bitcoincom
        self.obj = bitfinex
        self.obj = bitfinex2
        self.obj = bitflyer
        self.obj = bitforex
        self.obj = bitget
        self.obj = bithumb
        self.obj = bitmart
        self.obj = bitmex
        self.obj = bitopro
        self.obj = bitpanda
        self.obj = bitrue
        self.obj = bitso
        self.obj = bitstamp
        self.obj = bitstamp1
        self.obj = bittrex
        self.obj = bitvavo
        self.obj = bkex
        self.obj = bl3p
        self.obj = blockchaincom
        self.obj = btcalpha
        self.obj = btcbox
        self.obj = btcex
        self.obj = btcmarkets
        self.obj = btctradeua
        self.obj = btcturk
        self.obj = buda
        self.obj = bw
        self.obj = bybit
        self.obj = bytetrade
        self.obj = cex
        self.obj = coinbase
        self.obj = coinbaseprime
        self.obj = coinbasepro
        self.obj = coincheck
        self.obj = coinex
        self.obj = coinfalcon
        self.obj = coinmate
        self.obj = coinone
        self.obj = coinspot
        self.obj = crex24
        self.obj = cryptocom
        self.obj = currencycom
        self.obj = delta
        self.obj = deribit
        self.obj = digifinex
        self.obj = exmo
        self.obj = flowbtc
        self.obj = fmfwio
        self.obj = ftx
        self.obj = ftxus
        self.obj = gate
        self.obj = gateio
        self.obj = gemini
        self.obj = hitbtc
        self.obj = hitbtc3
        self.obj = hollaex
        self.obj = huobi
        self.obj = huobijp
        self.obj = huobipro
        self.obj = idex
        self.obj = independentreserve
        self.obj = indodax
        self.obj = itbit
        self.obj = kraken
        self.obj = kucoin
        self.obj = kucoinfutures
        self.obj = kuna
        self.obj = latoken
        self.obj = lbank
        self.obj = lbank2
        self.obj = liquid
        self.obj = luno
        self.obj = lykke
        self.obj = mercado
        self.obj = mexc
        self.obj = mexc3
        self.obj = ndax
        self.obj = novadax
        self.obj = oceanex
        self.obj = okcoin
        self.obj = okex
        self.obj = okex5
        self.obj = okx
        self.obj = paymium
        self.obj = phemex
        self.obj = poloniex
        self.obj = probit
        self.obj = qtrade
        self.obj = ripio
        self.obj = stex
        self.obj = therock
        self.obj = tidebit
        self.obj = tidex
        self.obj = timex
        self.obj = tokocrypto
        self.obj = upbit
        self.obj = wavesexchange
        self.obj = wazirx
        self.obj = whitebit
        self.obj = woo
        self.obj = yobit
        self.obj = zaif
        self.obj = zb
        self.obj = zipmex
        self.obj = zonda
        
        # Python 3.10
        # match name:
        #     case "binance":
        #         self._obj = binance
        #     case "coinbase":
        #         self._obj = coinbase
        #     case _:
        #         raise NotImplementedError(f"the {name=} does not exist for AbstractedObject.__init__")

    # used only by this class. Not used by the rest of your program ever. `_` in the name beginning indicates it being private.
    # since it is for private class usage, it can return internal complex values of cttx, or having them as input
    def _private_method_to_receive_intermediate_result(self, parameter1) -> None:
        return self.obj.convert_exchange_name_to_internal_nickname(parameter1)

    # public method to be used by the rest of your program
    # for input and output, only python default types and dataclasses/pydantic BadeModels or classes created by us are allowed (which follow same principles)
    def get_market(self, parameter1: str) -> list[MarketValue]:
        return [MarketValue(param1=val.bla, param2=val.bla2, param3=val.bla3) for val in self._obj.get_market_values(parameter1)]
    
    # public method to be used by the rest of your program
    # for input and output, only python default types and dataclasses/pydantic BadeModels or classes created by us are allowed (which follow same principles)
    def get_exchange(self, parameter1: str) -> float:
        parameter2 = self._private_method_to_receive_intermediate_result
        return self._obj.get_exchange_rate(parameter1, parameter2)


exchanges = AbstractedMarket()



# EXCH_MAP: dict[str, Type[ccxt.Exchange]] = {
#     'aax':ccxtpro.aax({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'alpaca':ccxtpro.alpaca({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'ascendex':ccxtpro.ascendex({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bequant':ccxtpro.bequant({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bibox':ccxtpro.bibox({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bigone':ccxtpro.bigone({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'binance':ccxtpro.binance({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'binancecoinm':ccxtpro.binancecoinm({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'binanceus':ccxtpro.binanceus({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'binanceusdm':ccxtpro.binanceusdm({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bit2c':ccxtpro.bit2c({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bitbank':ccxtpro.bitbank({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bitbay':ccxtpro.bitbay({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bitbns':ccxtpro.bitbns({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bitcoincom':ccxtpro.bitcoincom({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bitfinex':ccxtpro.bitfinex({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bitfinex2':ccxtpro.bitfinex2({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bitflyer':ccxtpro.bitflyer({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bitforex':ccxtpro.bitforex({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bitget':ccxtpro.bitget({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bithumb':ccxtpro.bithumb({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bitmart':ccxtpro.bitmart({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bitmex':ccxtpro.bitmex({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bitopro':ccxtpro.bitopro({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bitpanda':ccxtpro.bitpanda({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bitrue':ccxtpro.bitrue({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bitso':ccxtpro.bitso({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bitstamp':ccxtpro.bitstamp({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bitstamp1':ccxtpro.bitstamp1({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bittrex':ccxtpro.bittrex({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bitvavo':ccxtpro.bitvavo({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bkex':ccxtpro.bkex({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bl3p':ccxtpro.bl3p({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'blockchaincom':ccxtpro.blockchaincom({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'btcalpha':ccxtpro.btcalpha({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'btcbox':ccxtpro.btcbox({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'btcex':ccxtpro.btcex({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'btcmarkets':ccxtpro.btcmarkets({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'btctradeua':ccxtpro.btctradeua({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'btcturk':ccxtpro.btcturk({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'buda':ccxtpro.buda({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bw':ccxtpro.bw({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bybit':ccxtpro.bybit({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'bytetrade':ccxtpro.bytetrade({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'cex':ccxtpro.cex({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'coinbase':ccxtpro.coinbase({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'coinbaseprime':ccxtpro.coinbaseprime({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'coinbasepro':ccxtpro.coinbasepro({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'coincheck':ccxtpro.coincheck({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'coinex':ccxtpro.coinex({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'coinfalcon':ccxtpro.coinfalcon({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'coinmate':ccxtpro.coinmate({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'coinone':ccxtpro.coinone({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'coinspot':ccxtpro.coinspot({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'crex24':ccxtpro.crex24({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'cryptocom':ccxtpro.cryptocom({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'currencycom':ccxtpro.currencycom({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'delta':ccxtpro.delta({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'deribit':ccxtpro.deribit({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'digifinex':ccxtpro.digifinex({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'exmo':ccxtpro.exmo({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'flowbtc':ccxtpro.flowbtc({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'fmfwio':ccxtpro.fmfwio({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'ftx':ccxtpro.ftx({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'ftxus':ccxtpro.ftxus({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'gate':ccxtpro.gate({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'gateio':ccxtpro.gateio({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'gemini':ccxtpro.gemini({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'hitbtc':ccxtpro.hitbtc({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'hitbtc3':ccxtpro.hitbtc3({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'hollaex':ccxtpro.hollaex({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'huobi':ccxtpro.huobi({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'huobijp':ccxtpro.huobijp({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'huobipro':ccxtpro.huobipro({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'idex':ccxtpro.idex({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'independentreserve':ccxtpro.independentreserve({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'indodax':ccxtpro.indodax({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'itbit':ccxtpro.itbit({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'kraken':ccxtpro.kraken({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'kucoin':ccxtpro.kucoin({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'kucoinfutures':ccxtpro.kucoinfutures({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'kuna':ccxtpro.kuna({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'latoken':ccxtpro.latoken({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'lbank':ccxtpro.lbank({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'lbank2':ccxtpro.lbank2({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'liquid':ccxtpro.liquid({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'luno':ccxtpro.luno({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'lykke':ccxtpro.lykke({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'mercado':ccxtpro.mercado({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'mexc':ccxtpro.mexc({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'mexc3':ccxtpro.mexc3({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'ndax':ccxtpro.ndax({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'novadax':ccxtpro.novadax({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'oceanex':ccxtpro.oceanex({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'okcoin':ccxtpro.okcoin({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'okex':ccxtpro.okex({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'okex5':ccxtpro.okex5({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'okx':ccxtpro.okx({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'paymium':ccxtpro.paymium({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'phemex':ccxtpro.phemex({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'poloniex':ccxtpro.poloniex({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'probit':ccxtpro.probit({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'qtrade':ccxtpro.qtrade({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'ripio':ccxtpro.ripio({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'stex':ccxtpro.stex({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'therock':ccxtpro.therock({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'tidebit':ccxtpro.tidebit({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'tidex':ccxtpro.tidex({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'timex':ccxtpro.timex({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'tokocrypto':ccxtpro.tokocrypto({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'upbit':ccxtpro.upbit({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'wavesexchange':ccxtpro.wavesexchange({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'wazirx':ccxtpro.wazirx({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'whitebit':ccxtpro.whitebit({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'woo':ccxtpro.woo({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'yobit':ccxtpro.yobit({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'zaif':ccxtpro.zaif({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'zb':ccxtpro.zb({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'zipmex':ccxtpro.zipmex({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
#     'zonda':ccxtpro.zonda({'newUpdates': False, 'apiKey':self.config['exchanges'][exchange]['apiKey'], 'secret':self.config['exchanges'][exchange]['secret']}),
# }