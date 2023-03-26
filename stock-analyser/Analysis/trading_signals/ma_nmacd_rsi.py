
import pandas
from talib import abstract


import sys
sys.path.append('..')
from Analysis.utils import IndicatorUtils
import  Analysis.Indicator.nmacd as nmacd

class MaNmacdRsi(IndicatorUtils):
    def analyze(self, historical_data):
        """MA13+NMACD+RSI STATEGY

        Args:
            historical_data (list): A matrix of historical OHCLV data.
            signal (list, optional): Defaults to sma,ma_norm,trigger,rsi,rsi_sma. The indicator line to check hot/cold
                against.
            hot_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to purchase.
            cold_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to sell.

        Returns:
            pandas.DataFrame: A dataframe containing the indicators and hot/cold values.
        """
        results={'is_hot':False,'is_cold':False,'ma_nmacd_rsi':{}}

        dataframe = self.convert_to_dataframe(historical_data)

        #SMA13
        sma_values = abstract.SMA(dataframe, 13).to_frame()
        sma_values.dropna(how='all', inplace=True)
        sma_values.rename(columns={0: 'sma'}, inplace=True)

        up_sma = dataframe['close'][-1]> sma_values['sma'][-1]
        down_sma = dataframe['close'][-1] < sma_values['sma'][-1]

        up_sma_pre = dataframe['close'][-2] > sma_values['sma'][-2]
        down_sma_pre = dataframe['close'][-2] < sma_values['sma'][-2]



        #nmacd
        nmacd_values =nmacd.nmacd(dataframe,fastma_period=13,slowma_period=21,trigger_period=9,normalize_period=50)
        nmacd_hot = nmacd_values['macnorm2']>nmacd_values['trigger']
        nmacd_cold = nmacd_values['macnorm2']<nmacd_values['trigger']

        #rsi21
        rsi_values = abstract.RSI(dataframe, 21).to_frame()
        rsi_values.dropna(how='all', inplace=True)
        rsi_values.rename(columns={rsi_values.columns[0]: 'close'}, inplace=True)


        #rsi_sma
        rsi_sma = abstract.SMA(rsi_values,55).to_frame()
        rsi_sma.dropna(how='all',inplace=True)
        rsi_sma.rename(columns={rsi_sma.columns[0]:'rsi_sma'},inplace=True)

        cross_up_rsi = rsi_values['close'][-2] < rsi_sma['rsi_sma'][-2] and rsi_values['close'][-1] > rsi_sma['rsi_sma'][-1]
        cross_down_rsi = rsi_values['close'][-2] > rsi_sma['rsi_sma'][-2] and rsi_values['close'][-1] < rsi_sma['rsi_sma'][-1]

        cross_up_rsi_pre = rsi_values['close'][-3] < rsi_sma['rsi_sma'][-3] and rsi_values['close'][-2] > \
                       rsi_sma['rsi_sma'][-2]

        cross_down_rsi_pre = rsi_values['close'][-3] > rsi_sma['rsi_sma'][-3] and rsi_values['close'][-2] < \
                         rsi_sma['rsi_sma'][-2]





        is_hot = False
        is_cold = False
        make_sure = 0
        #if up_sma and cross_up_rsi and nmacd_hot[-1] and in_alerttime:
        #   is_hot = True

        #if down_sma and cross_down_rsi and nmacd_cold[-1] and in_alerttime:
        #   is_cold = True


        #make sure

        if up_sma_pre and cross_up_rsi_pre and nmacd_hot[-2]:
            is_hot = True
            make_sure = 1

        if down_sma_pre and cross_down_rsi_pre and nmacd_cold[-2]:
            is_cold = True
            make_sure = 1

        results['is_hot'] = is_hot
        results['is_cold'] = is_cold




        results['ma_nmacd_rsi']['values']={}
        results['ma_nmacd_rsi']['values']['peroid'] = dataframe.index[-1] - dataframe.index[-2]
        results['ma_nmacd_rsi']['values']['is_hot'] = is_hot
        results['ma_nmacd_rsi']['values']['is_cold'] = is_cold
        results['ma_nmacd_rsi']['values']['make_sure'] = make_sure
        results['ma_nmacd_rsi']['values']['close'] = dataframe['close'][-2]
        results['ma_nmacd_rsi']['values']['high'] = dataframe['high'][-2]
        results['ma_nmacd_rsi']['values']['low'] = dataframe['low'][-2]
        results['ma_nmacd_rsi']['values']['sma'] = sma_values['sma'][-2]
        results['ma_nmacd_rsi']['values']['rsi_pre'] = rsi_values['close'][-3]
        results['ma_nmacd_rsi']['values']['rsi'] = rsi_values['close'][-2]
        results['ma_nmacd_rsi']['values']['sma_rsi_pre'] = rsi_sma['rsi_sma'][-3]
        results['ma_nmacd_rsi']['values']['sma_rsi'] = rsi_sma['rsi_sma'][-2]
        results['ma_nmacd_rsi']['values']['macnorm2'] = nmacd_values['macnorm2'][-3]
        results['ma_nmacd_rsi']['values']['trigger'] =nmacd_values['trigger'][-2]


        #df_results=pandas.DataFrame(results)
        return results






