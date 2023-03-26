import re
import pandas
import datetime
from talib import abstract


import sys
sys.path.append('..')
from Analysis.utils import IndicatorUtils
import  Analysis.Indicator.HullSuite as HullSuite
import  Analysis.Indicator.HalfTrend as HalfTrend

class HHC(IndicatorUtils):
    def analyze(self, historical_data):
        """HULLSUITE+HALFTREND+CCI STATEGY

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
        results={'is_hot':False,'is_cold':False,'hhc':{}}
        dataframe = self.convert_to_dataframe(historical_data)
        hs=HullSuite.hullsuite(dataframe)
        ht = HalfTrend.halftrend(dataframe)
        cci = abstract.CCI(dataframe,14)
        ht_buy = ht['trend'].iloc[-1] == 0 and ht['trend'].iloc[-2] == 1
        ht_sell = ht['trend'].iloc[-1] == 1 and ht['trend'].iloc[-2] == 0
        is_hot = False
        is_cold = False
        make_sure = 0




        # make_sure
        ht_buy_pre = ht['trend'].iloc[-2] == 0 and ht['trend'].iloc[-3] == 1
        ht_sell_pre = ht['trend'].iloc[-2] == 1 and ht['trend'].iloc[-3] == 0
        # buy_condition make sure
        if ht_buy_pre and hs['hot_cold'].iloc[-2] > 0 and ht['ht'].iloc[-2] > hs['hma'].iloc[-2] and cci.iloc[-2] > -200 and \
                cci.iloc[-2] < 200:
            is_hot = True
            make_sure = 1

         # sell condition make sure
        if ht_sell_pre and hs['hot_cold'].iloc[-2] < 0 and ht['ht'].iloc[-2] < hs['hma'].iloc[-2] and cci.iloc[
            -2] > -200 and cci.iloc[-2] < 200:
            is_cold = True
            make_sure =1

        results['is_hot'] = is_hot
        results['is_cold'] = is_cold

        results['hhc']['values'] = {}


        results['hhc']['values']['peroid'] = dataframe.index[-1] - dataframe.index[-2]
        results['hhc']['values']['is_hot'] = is_hot
        results['hhc']['values']['is_cold'] = is_cold
        results['hhc']['values']['make_sure'] = make_sure
        results['hhc']['values']['close'] = dataframe['close'][-2]
        results['hhc']['values']['high'] = dataframe['high'][-2]
        results['hhc']['values']['low'] = dataframe['low'][-2]
        results['hhc']['values']['ht_buy'] = ht_buy_pre
        results['hhc']['values']['ht_sell'] = ht_sell_pre
        results['hhc']['values']['hs_hot_cold'] = hs['hot_cold'].iloc[-2]
        results['hhc']['values']['ht'] = ht['ht'].iloc[-2]
        results['hhc']['values']['hma'] = hs['hma'].iloc[-2]
        results['hhc']['values']['cci'] = cci.iloc[-2]
        #df_results = pandas.DataFrame(results)
        return results
