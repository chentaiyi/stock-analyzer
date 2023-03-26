import talib
import pandas

def macd(dataframe, fastma_period=13,slowma_period=26,signal_period=9):
    (macd,macd_signal,macd_hist) =talib.MACD(dataframe['close'],fastperiod=fastma_period, slowperiod=slowma_period, signalperiod=signal_period,)

    df = pandas.DataFrame(dataframe['close'])
    df['dif'] = macd
    df['dea']= macd_signal
    df['macd'] =macd_hist
    return df