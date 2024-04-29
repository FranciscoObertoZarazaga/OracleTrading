def SqueezeStrategy(df, n):
    isSM = df['isSM'][n]
    sm = df['sm'][n]
    sm_past = df['sm'][n-1]
    sm_past_2 = df['sm'][n-2]
    adx = df['adx'][n]
    adx_past = df['adx'][n-1]
    adx_past_2 = df['adx'][n-2]
    if adx < adx_past and adx_past_2 < adx_past:
        if sm < 0:
            return 1
        else:
            return -1
    if adx_past < adx and adx_past < adx_past_2:
        return 0
    return 0

def CrossingOfMeansStrategy(slow_mean, speed_mean, n):
    if speed_mean[n] >= slow_mean[n] and slow_mean[n-1] > speed_mean[n-1]:
        return +1
    elif slow_mean[n] >= speed_mean[n] and speed_mean[n-1] > slow_mean[n-1]:
        return -1
    return 0

def RSIStratygy(df,n):
    rsi = df['rsi']
    if rsi[n] > 70:
        return 1
    if rsi[n] < 30:
        return -1
    return 0

def BBStrategy(df, n):
    price = df['Close'][n]
    bbl = df['bbl'][n]
    bbh = df['bbh'][n]
    if price < bbl:
        return -1
    if price > bbh:
        return 1
    return 0

def TrendStrategy(df,t):
    price = df['Close']
    if price[t] > price[t-1]:
        return 1
    else:
        return -1


def WinStrategy(df, n):
    adx = df['adx']
    sm = df['sm']
    sma = df['sma']
    ema = df['ema']
    isSm = df['isSm']
    price = df['Close']
    isMin = adx[n] > adx[n-1] and adx[n-2] > adx[n-1]
    isMax = adx[n] < adx[n - 1] and adx[n - 2] < adx[n - 1]
    isUp = price[n] > sma[n]
    isMagic = sm[n] > sm[n-1]

    if isMin:
        if adx[n-1] < 30:
            if isMagic:
                return 1
            if isUp:
                return 1
            return -1


    if adx[n] < 30:
        if isUp and price[n-1] < sma[n-1] and isMagic:
            return 1

    return 0


def StableSqueezeStrategy(df, n):
    adx = df['adx']
    sm = df['sm']
    if adx[n] > 70:
        return -1 if sm[n] > sm[n-1] else 1
    elif adx[n] < 30:
        return 1 if sm[n] > sm[n-1] else -1
    return 0

def GodStrategy(df, n, y):
    price = df['Close']
    #y = price[n] < price[n+1]
    if y == None:
        return 0
    if price[n] < price[n-1] and y:
        return 1
    if price[n] > price[n-1] and not y:
        return -1
    return 0

def NovechentaStrategy(df,t):
    adx = df['adx']
    sm = df['sm']

    #Si el adx alcanza un mínimo o un máximo
    if (adx[t] < adx[t-1] and adx[t-2] < adx[t-1]) or (adx[t] > adx[t-1] and adx[t-2] > adx[t-1]) and df['sma'][t] < df['Close'][t]:
        #Si el monitor es bajista con direccion alcista
        if sm[t] > sm[t-1] and sm[t] < 0:
            return 1
        #Si el monitor es alcista con direccion bajista
        if sm[t] < sm[t-1] and sm[t] > 0:
            return -1
    return 0

def GeranatorStrategy(df, n):
    adx = df['adx']
    sm = df['sm']
    di_pos = df['di+']
    di_neg = df['di-']
    isMin = adx[n] > adx[n - 1] and adx[n - 2] > adx[n - 1]
    if isMin:
        if adx[n] < 30 and adx[n] > 20:
            if di_pos[n] > di_neg[n]:
                return 1
            if di_pos[n] < di_neg[n]:
                return -1
    return 0