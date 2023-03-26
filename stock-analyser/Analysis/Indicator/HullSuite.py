import pandas
import numpy as np
from talib import abstract


def hullsuite(dataframe,length=55,length_mult=1):

    hma = abstract.WMA(2*abstract.WMA(dataframe,round(length*length_mult /2)-1)-abstract.WMA(dataframe,length*length_mult),round(np.sqrt(length*length_mult)))
    df_hma=pandas.DataFrame(hma)
    df_hma.dropna(how='all', inplace=True)
    df_hma.rename(columns={0: 'hma'}, inplace=True)
    df_hma['hot_cold'] = df_hma.diff(periods=2,axis=0)
    return df_hma