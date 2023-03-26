
import pandas

from analyzers.utils import IndicatorUtils
import sys
sys.path.append('..')
from Analysis.Indicator import Smart_Money_Concepts

class SmartMoneyConcepts(IndicatorUtils):
    def analyze(self, historical_data, signal=['smart_money_concepts'],hot_thresh=None, cold_thresh=None,time_unit = '1h'):
        """smart money concepts STATEGY

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

        results = {'is_hot': False, 'is_cold': False, 'smc': {}}
        dataframe = self.convert_to_dataframe(historical_data)
        ob_blocks = Smart_Money_Concepts.smart_money_concepts(dataframe,50,5)
        is_hot  =False
        is_cold = False

        close = dataframe['close'][-1]
        close_pre = dataframe['close'][-2]

        iob_type = 0
        iob_top =0.0
        iob_btm = 0.0
        iob_timestamp = 0

        ob_blocks.reverse()

        for data in ob_blocks:
            #支撑区域
            if data['iob_type'] == 1:
                #进入支撑区域
                if close_pre > (data['iob_top'] + data['iob_btm'])/2 and close < (data['iob_top'] + data['iob_btm'])/2:
                    iob_top = data['iob_top']
                    iob_type = 1
                    is_hot = True
                    iob_timestamp = data['iob_left']
                    break
            #压力区域
            if data['iob_type'] == -1:
            #进入压力区域
                if close_pre < (data['iob_top'] + data['iob_btm'])/2 and close > (data['iob_top'] + data['iob_btm'])/2:
                    iob_btm = data['iob_btm']
                    iob_type = -1
                    is_cold = True
                    iob_timestamp = data['iob_left']
                    break

        results['is_hot'] = is_hot
        results['is_cold'] = is_cold

        results['smc']['values'] = {}
        results['smc']['values']['is_hot'] = is_hot
        results['smc']['values']['is_cold'] = is_cold
        results['smc']['values']['peroid'] = dataframe.index[-1] - dataframe.index[-2]
        results['smc']['values']['iob_time'] = iob_timestamp
        results['smc']['values']['iob_type'] = iob_type
        results['smc']['values']['iob_top'] = iob_top
        results['smc']['values']['iob_btm'] = iob_btm
        results['smc']['values']['close_pre'] =close_pre
        results['smc']['values']['close'] = close

        df_results = pandas.DataFrame(results)
        return df_results