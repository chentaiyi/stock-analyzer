import pandas
from talib import abstract


def halftrend(dataframe,amplitude=2):

    highest = dataframe['high'].rolling(amplitude).max()
    df = pandas.DataFrame(highest)
    lowest = dataframe['low'].rolling(amplitude).min()
    df2 = pandas.DataFrame(lowest)
    #highma = abstract.SMA(df,amplitude).to_frame()
    #lowma = abstract.SMA(df2,amplitude).to_frame()
    highma = abstract.SMA(dataframe['high'], amplitude)
    lowma = abstract.SMA(dataframe['low'], amplitude)
    df.rename(columns={df.columns[0]: 'highest'}, inplace=True)
    df2.rename(columns={df2.columns[0]: 'lowest'}, inplace=True)
    df_all = pandas.DataFrame()
    df_all['low'] = dataframe['low']
    df_all['close'] = dataframe['close']
    df_all['high'] =dataframe['high']
    df_all['highest'] = df
    df_all['lowest'] = df2
    df_all['highma'] = highma
    df_all['lowma'] = lowma
    trend = [0]
    next_trend = 0
    up =[0.0]
    down = [0.0]
    maxLowPrice = df_all['low'][0]
    minHighPrice = df_all['high'][0]
    data_cache=[]
    ht=[]
    count = 0
    for data in df_all.itertuples():
        trend_now = trend[-1]
        up_now = up[-1]
        down_now = down[-1]
        if len(data_cache) >1:
            data_cache.pop(0)
        data_cache.append(data)
        if next_trend == 1:
            maxLowPrice = max(data[5],maxLowPrice)
            if len(data_cache) >1:
                low = data_cache[-2][1]
            else:
                low = data_cache[-1][1]
            if data[6] < maxLowPrice and data[2] < low:
                trend_now = 1
                next_trend = 0
                minHighPrice = data[4]
        else:
            minHighPrice = min(data[4],minHighPrice)
            if len(data_cache) >1:
                high = data_cache[-2][3]
            else:
                high = data_cache[-1][3]
            if data[7] >minHighPrice and data[2] > high:
                trend_now = 0
                next_trend = 1
                maxLowPrice = data[5]
        if count !=0:
            trend.append(trend_now)
        else:
            trend[0] = trend_now
        if trend[-1] ==0:
            if len(trend) > 1 and trend[-2]!=0:
                up_now = down[-1]
            else:
                if len(up) >1:
                    up_now=max(maxLowPrice, up[-1])
                else:
                    up_now = maxLowPrice

        else:
             if len(trend) > 1 and trend[-2]!=1:
                 down_now = up[-1]
             else:
                 if len(down) >1:
                     down_now = min(minHighPrice, down[-1])
                 else:
                     down_now = minHighPrice
        if count!=0:
            up.append(up_now)
        else:
            up[0] = up_now
        if count!=0:
            down.append(down_now)
        else:
            down[0] = down_now
        if trend[-1] == 0:
            ht.append(up[-1])
        else:
            ht.append(down[-1])
        if count == 0:
            count +=1
    df_ht = pandas.DataFrame(ht)
    df_ht.dropna(how='all', inplace=True)
    df_ht.rename(columns={0: 'ht'}, inplace=True)
    df_ht['trend'] = trend
    return df_ht
















