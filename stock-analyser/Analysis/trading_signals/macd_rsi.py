import pandas
from talib import abstract


import sys
sys.path.append('..')
from Analysis.utils import IndicatorUtils
import  Analysis.Indicator.macd as macd

class MacdRsi(IndicatorUtils):
    def analyze(self, historical_data):
        """MACD+RSI STATEGY

        Args:
            historical_data (list): A matrix of historical OHCLV data.
            signal (list, optional): Defaults to macd,rsi, The indicator line to check hot/cold
                against.
            hot_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to purchase.
            cold_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to sell.

        Returns:
            pandas.DataFrame: A dataframe containing the indicators and hot/cold values.
        """
        results={'is_hot':False,'is_cold':False,'mr':{}}

        dataframe = self.convert_to_dataframe(historical_data)

        #macd
        df_macd = macd.macd(dataframe,fastma_period=12,slowma_period=26,signal_period=9)
        df_macd.dropna(how='all', inplace=True)

        macd_hot =df_macd['dif'][-1] < 0 and df_macd['dea'][-1] < 0 and \
                  df_macd['dif'][-2] < df_macd['dea'][-2] and \
                  df_macd['dif'][-1] >df_macd['dea'][-1]
        macd_cold =df_macd['dif'][-1] > 0 and df_macd['dea'][-1] > 0 and \
                  df_macd['dif'][-2] > df_macd['dea'][-2] and \
                  df_macd['dif'][-1] <df_macd['dea'][-1]

        macd_hot_pre = df_macd['dif'][-2] < 0 and df_macd['dea'][-2] < 0 and \
                  df_macd['dif'][-3] < df_macd['dea'][-3] and \
                  df_macd['dif'][-2] >df_macd['dea'][-2]

        macd_cold_pre = df_macd['dif'][-2] > 0 and df_macd['dea'][-2] > 0 and \
                    df_macd['dif'][-3] > df_macd['dea'][-3] and \
                    df_macd['dif'][-2] < df_macd['dea'][-2]

        #rsi21
        rsi_values = abstract.RSI(dataframe, 21).to_frame()
        rsi_values.dropna(how='all', inplace=True)
        rsi_values.rename(columns={rsi_values.columns[0]: 'close'}, inplace=True)

        # rsi_sma
        rsi_sma = abstract.SMA(rsi_values, 55).to_frame()
        rsi_sma.dropna(how='all', inplace=True)
        rsi_sma.rename(columns={rsi_sma.columns[0]: 'rsi_sma'}, inplace=True)

        cross_up_rsi = rsi_values['close'][-2] < rsi_sma['rsi_sma'][-2] and rsi_values['close'][-1] > \
                       rsi_sma['rsi_sma'][-1]
        cross_down_rsi = rsi_values['close'][-2] > rsi_sma['rsi_sma'][-2] and rsi_values['close'][-1] < \
                         rsi_sma['rsi_sma'][-1]

        cross_up_rsi_pre = rsi_values['close'][-3] < rsi_sma['rsi_sma'][-3] and rsi_values['close'][-2] > \
                           rsi_sma['rsi_sma'][-2]

        cross_down_rsi_pre = rsi_values['close'][-3] > rsi_sma['rsi_sma'][-3] and rsi_values['close'][-2] < \
                             rsi_sma['rsi_sma'][-2]





        is_hot = False
        is_cold = False
        make_sure = 0
        if macd_hot and cross_up_rsi:
           is_hot = True

        if macd_cold and cross_down_rsi:
           is_cold = True

        # make sure

        if macd_hot_pre and cross_up_rsi_pre:
            is_hot = True
            make_sure = 1

        if macd_cold_pre and cross_down_rsi_pre:
            is_cold = True
            make_sure = 1

        results['is_hot'] = is_hot
        results['is_cold'] = is_cold




        results['mr']['values']={}
        results['mr']['values']['peroid'] = dataframe.index[-1] - dataframe.index[-2]
        results['mr']['values']['is_hot'] = is_hot
        results['mr']['values']['is_cold'] = is_cold
        results['mr']['values']['make_sure'] = make_sure
        results['mr']['values']['close'] = dataframe['close'][-2]
        results['mr']['values']['high'] = dataframe['high'][-2]
        results['mr']['values']['low'] = dataframe['low'][-2]
        results['mr']['values']['rsi_pre'] = rsi_values['close'][-3]
        results['mr']['values']['rsi'] = rsi_values['close'][-2]
        results['mr']['values']['sma_rsi_pre'] = rsi_sma['rsi_sma'][-3]
        results['mr']['values']['sma_rsi'] = rsi_sma['rsi_sma'][-2]
        results['mr']['values']['dif'] = df_macd['dif'][-2]
        results['mr']['values']['dea'] =df_macd['dea'][-2]


        #df_results=pandas.DataFrame(results)
        return results