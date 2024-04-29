import time
from binance.client import Client
from binance import ThreadedWebsocketManager

API_KEY = ""
SECRET_KEY = ""

class Binance:

    def __init__(self):
        self.client = Client(API_KEY, SECRET_KEY)

    def getAllTickers(self):
        return self.client.get_all_tickers()

    #Retorna un listado de cryptomonedas disponibles en Binance
    def getAllCoins(self):
        return self.client.get_all_coins_info()

    def getClient(self):
        return self.client

    def getStatus(self):
        return self.client.get_system_status()

    #Devuelve el libro de órdenes de compra y venta.
    #El Bid price es el precio máximo al que un consumidor está dispuesto a comprar
    # El Ask price es el precio mínimo al que un oferente está dispuesto a vender
    def getOrderBook(self,symbol):
        try:
            return self.client.get_order_book(symbol=symbol,limit="1000")
        except:
            self.reconnect()
            return self.getOrderBook(symbol)

    def get_mean(self,symbol):
        try:
            return float(self.client.get_avg_price(symbol=symbol)['price'])
        except:
            self.reconnect()
            return self.get_price(symbol)

    def get_price(self,symbol):
        try:
            order_book = self.client.get_order_book(symbol=symbol,limit="1")
            #return buy_price, sell_price
            return float(order_book['asks'][0][0]), float(order_book['bids'][0][0])
        except:
            self.reconnect()
            return self.get_price(symbol)

    def get_historical_k_lines(self,symbol,interval,start_str,end_str=None):
        return self.client.get_historical_klines(symbol, interval, start_str,end_str)

    def get_k_lines(self,symbol,interval):
        return self.client.get_klines(symbol=symbol, interval=interval)

    def reconnect(self,n=1):
        try:
            if n==1:
                print("Reconectando")
            self.getStatus()
        except:
            time.sleep(10)
            self.reconnect(0)

    def alert(self,msg):
        print('Recibido',msg)


class WebSocketBinance:
    def __init__(self):
        self.ws = ThreadedWebsocketManager(api_key=API_KEY, api_secret=SECRET_KEY)
        self.ws.start()
        self.observers = list()

    def subscribe(self,observer):
        self.observers.append(observer)

    def notify(self,data):
        for observer in self.observers: observer.update(data)

    def add(self,symbol,interval):
        self.ws.start_kline_socket(callback=self.notify, symbol=symbol,interval=interval)
