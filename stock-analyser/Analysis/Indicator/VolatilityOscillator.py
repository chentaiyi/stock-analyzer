import pandas



def volatility_oscillator(dataframe,peroid=100):
    df=pandas.DataFrame()
    df['spike'] = dataframe.apply(lambda x: x['close'] - x['open'],axis=1)
    df['upper_line'] = df['spike'].rolling(peroid).std(ddof=0)
    df['lower_line'] = -df['spike'].rolling(peroid).std(ddof=0)
    return df