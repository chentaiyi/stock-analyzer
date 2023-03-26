import pandas
from talib import abstract
import math

def ssl_channel(dataframe,hperiod = 21,lperiod=21):
    df_high = pandas.DataFrame(dataframe['high'])
    df_high.rename(columns={'high': 'close'}, inplace=True)
    df_low = pandas.DataFrame(dataframe['low'])
    df_low.rename(columns={'low': 'close'}, inplace=True)
    high_sma = abstract.SMA(df_high, hperiod).to_frame()
    high_sma.rename(columns={0: 'high_sma'}, inplace=True)
    low_sma = abstract.SMA(df_low, lperiod).to_frame()
    low_sma.rename(columns={0: 'low_sma'}, inplace=True)
    df = pandas.DataFrame(dataframe['close'])
    df['high_sma'] = high_sma['high_sma']
    df['low_sma'] = low_sma['low_sma']

    hlv=[]
    for data in df.itertuples():
        if math.isnan(data[2]) or math.isnan(data[3]):
            hlv.append(float('nan'))
        else:
            if data[1] > data[2]:
                hlv_value = 1
            else:
                if data[1] < data[3]:
                    hlv_value =-1
                else:
                    if len(hlv) >0:
                        hlv_value = hlv[-1]
                    else:
                        hlv_value = float('nan')
            hlv.append(hlv_value)
    df['hlv'] = hlv
    df['ssl_down'] = df.apply(lambda x:x['high_sma'] if x['hlv'] < 0 else x['low_sma'],axis=1)
    df['ssl_up'] = df.apply(lambda x: x['low_sma'] if x['hlv'] < 0 else x['high_sma'],axis=1)
    return df


