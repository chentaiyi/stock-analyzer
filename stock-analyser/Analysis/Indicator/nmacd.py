import pandas
from talib import abstract


def nmacd(dataframe, fastma_period=13,slowma_period=9,trigger_period=9,normalize_period=50):

    # manorm
    fastma = abstract.EMA(dataframe, fastma_period).to_frame()
    fastma.dropna(how='all', inplace=True)
    fastma.rename(columns={0: 'fastma'}, inplace=True)

    slowma = abstract.EMA(dataframe, slowma_period).to_frame()
    slowma.dropna(how='all', inplace=True)
    slowma.rename(columns={0: 'slowma'}, inplace=True)

    df = pandas.concat([fastma['fastma'],slowma['slowma']],axis=1,join='inner')
    df['mac'] = df.apply(_mac,axis=1)
    df['minmac'] = abstract.MIN(df['mac'],normalize_period)
    df['maxmac'] = abstract.MAX(df['mac'],normalize_period)
    df['macnorm'] = df.apply(_macnorm,axis=1)
    df['macnorm2'] = df.apply(_macnorm2,np=normalize_period,axis=1)
    df['trigger'] = abstract.WMA(df['macnorm2'],trigger_period)
    results=pandas.DataFrame(df[["macnorm2","trigger"]])
    results.dropna(how='all',inplace=True)
    return results
    #dfmac=dfma.apply(self._mac,axis=1)

def _mac(x):
    max_ma = max(x["fastma"], x["slowma"])
    if max != 0:
        radio = min(x["fastma"],x["slowma"])/max_ma
    t=0.0
    if x["fastma"] > x["slowma"]:
        t=2-radio
    else:
        t=radio
    mac=t-1
    return mac

def _macnorm(x):
    macnorm=((x['mac']-x['minmac']) /(x['maxmac']-x['minmac']+.000001)*2)- 1
    return macnorm

def _macnorm2(x,np):
    if np < 2:
        macnorm2 = x['mac']
    else:
        macnorm2 = x['macnorm']
    return macnorm2