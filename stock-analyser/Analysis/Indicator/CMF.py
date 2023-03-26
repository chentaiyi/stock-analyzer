import pandas

#Chaikin Money Flow
def cmf(dataframe,peroid=21):
    df = pandas.DataFrame()
    df['ad'] =dataframe.apply(lambda x:0 if x['close'] == x['high'] and
                              x['close'] == x['low'] or x['high'] == x['low']
                              else ((2*x['close']-x['low']-x['high'])/(x['high']-x['low']))
                                   *x['volume'],axis=1)
    df['volume'] = dataframe['volume']
    df['mf'] = df['ad'].rolling(peroid).sum()/df['volume'].rolling(peroid).sum()
    return df