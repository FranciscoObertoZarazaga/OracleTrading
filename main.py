import numpy as np

from SqueezeMomentumIndicator import *
from Indicator import *
from HistoricalKlines import HistoricalKlines
from Trader import Trader
from binance.enums import *
from datetime import datetime
from Strategy import *
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


symbol = 'BTCUSDT'
start_str = '7 year ago'
end_str = None
interval = KLINE_INTERVAL_15MINUTE
src = 'klines/15min_kline_btc.csv'

hk = HistoricalKlines(symbol=symbol,start_str=start_str,end_str=end_str, interval=interval,src=src)
kline = hk.getKlines()

#kline['sm'] = SqueezeMomentumIndicator(kline)
kline['adx'], kline['di+'], kline['di-'] = adxIndicator(kline)
kline['rsi'] = rsiIndicator(kline,20)
kline['sma'] = smaIndicator(kline,5)
kline['ema'] = emaIndicator(kline,10)
kline['bbh'], kline['bbm'], kline['bbl'] = bollingerBandsIndicator(kline)

kp = kline.iloc[:-1]['Close']
kf = kline.iloc[1:]['Close'].reset_index(drop=True)
kline.drop(len(kline)-1,inplace=True)
kline['future'] = np.where(kp < kf, True, False)
kline.dropna(inplace=True)
kline.reset_index(drop=True,inplace=True)

conditions = list()
#conditions.append(kline['Open'] > kline['Close'])
c = (kline['High'] - kline['Close'] < kline['Open'] - kline['Low'])
conditions.append(c)

condition = True
for c in conditions:
    condition = condition & c

kline['predict'] = np.where(condition, True, False)


result = kline[kline['future'] == kline['predict'] & (kline['predict'] != np.nan)]
kline = kline[kline['predict'] != np.nan]


print(f'Resultado:{len(result)/len(kline):.2%}')
print(len(kline))


trader = Trader(symbol)

buy_price = 0
signal = list()
for i in range(len(kline)):
    if i < 2 or i >= len(kline):
        signal.append(0)
        continue

    price = kline['Close'][i]
    time = kline.index[i]
    indoor = trader.indoor
    y = kline['predict'][i]

    points = 0
    points += GodStrategy(kline, i, y)
    points -= 1 if price < buy_price * .0 else 0

    if (indoor and points < 0) or (not indoor and points > 0):
        signal.append(points)
    else:
        signal.append(0)

    if points > 0:
        trader.buy(price,time)
        buy_price = price
    elif points < 0:
        trader.sell(price,time)
        buy_price = 0



last = len(kline) - 1
trader.sell(kline['Close'][last], kline.index[last])
kline['signal'] = signal
tiempo = datetime.strptime(kline['Time'][last], '%H:%M %d-%m-%Y') - datetime.strptime(kline['Time'][0], '%H:%M %d-%m-%Y')
print('#'*50)
print(f'SE SIMULARON {int(tiempo.days/365)} AÑOS, {int((tiempo.days % 365) / 31)} MESES Y{(tiempo.days % 365) % 31 + tiempo.seconds/86400: .2f} DÍAS')
print('#'*50)
print(trader)

rendimiento_diario = trader.wallet.rendimiento / (tiempo.days * 100)
print('#'*50)
print('RENDIMIENTO')
print(f'Diario:{rendimiento_diario: .2%}\nMensual:{rendimiento_diario * 30: .2%}\nAnual:{rendimiento_diario * 365: .2%}')
print('#'*50)


exit(0)
trades = trader.getSummaryTrades()

print(trades)

exit(1)
color = list()
size = list()
for i in kline['signal']:
    color.append('red' if i < 0 else ('green' if i > 0 else 'black'))
    size.append(25 if i != 0 else 0)
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
ax1.plot(kline.index, kline['Close'], linewidth=1)
ax1.scatter(kline.index, kline['Close'],color=color, s=size)
ax2.plot(kline.index, kline['sm'],c='blue')
ax2.plot(kline.index, kline['adx']*100-2000,c='red')
ax2.axhline(y=5, xmin=0.1, xmax=0.9)
plt.show()

