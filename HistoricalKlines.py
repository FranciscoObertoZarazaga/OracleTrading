import pandas as pd
from datetime import datetime
from Binance import Binance
import os

class HistoricalKlines:
    def __init__(self,symbol,interval,start_str,src,end_str=None):
        self.binance = Binance()
        self.klines = pd.DataFrame()
        self.symbol = symbol
        self.interval = interval
        self.start_str = start_str
        self.end_str = end_str
        self.src = src
        self.load()


    def load(self,):
        try:
            assert self.src is not None and os.path.exists(self.src)
            self.klines = pd.read_csv(self.src, index_col=0)
        except:
            self._download()
            self.save()

    def save(self):
        self.klines.to_csv(self.src)

    def getKlines(self):
        return self.klines

    def _download(self):
        colums, times = ['Time','Open','High','Low','Close','Volume','ignore','ignore','ignore','ignore','ignore','ignore'], list()
        self.klines = pd.DataFrame(self.binance.get_historical_k_lines(symbol=self.symbol,interval=self.interval,start_str=self.start_str,end_str=self.end_str),columns=colums)
        [times.append(datetime.fromtimestamp(int(str(time))/1000).strftime('%H:%M %d-%m-%Y')) for time in self.klines['Time']]
        self.klines['Time'] = times
        self.klines = self.klines.drop(['ignore','ignore','ignore','ignore','ignore','ignore'], axis=1)
        self.klines['mean'] = self.klines['Close'].rolling(window=20).mean()
        self.klines[['Open','High','Low','Close','Volume', 'mean']] = self.klines[['Open','High','Low','Close','Volume', 'mean']].astype(float)
