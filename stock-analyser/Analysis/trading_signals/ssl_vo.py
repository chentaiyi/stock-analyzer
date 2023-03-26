import pandas



import sys
sys.path.append('..')
from Analysis.utils import IndicatorUtils
import Analysis.Indicator.SslChannel as SslChannel
import Analysis.Indicator.VolatilityOscillator as VolatilityOscillator

class SslVo(IndicatorUtils):
    def analyze(self, historical_data):
        """SSL+VO STATEGY

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
        results={'is_hot':False,'is_cold':False,'sv':{}}
        dataframe = self.convert_to_dataframe(historical_data)
        ssl_channel = SslChannel.ssl_channel(dataframe)
        vo = VolatilityOscillator.volatility_oscillator(dataframe)


        is_hot = False
        is_cold = False
        make_sure = 0



        #maike sure
        if ssl_channel['ssl_up'][-3] < ssl_channel['ssl_down'][-3] and \
                ssl_channel['ssl_up'][-2] > ssl_channel['ssl_down'][-2]\
                and  vo['spike'][-2] > vo['upper_line'][-2]:
            is_hot =True
            make_sure = 1
        if ssl_channel['ssl_up'][-3] > ssl_channel['ssl_down'][-3] and \
                ssl_channel['ssl_up'][-2] < ssl_channel['ssl_down'][-2]\
                and vo['spike'][-2] < vo['lower_line'][-2]:

            is_cold = True
            make_sure = 1



        results['is_hot'] = is_hot
        results['is_cold'] = is_cold

        results['sv']['values'] = {}
        results['sv']['values']['peroid'] = dataframe.index[-1] - dataframe.index[-2]
        results['sv']['values']['is_hot'] = is_hot
        results['sv']['values']['is_cold'] = is_cold
        results['sv']['values']['make_sure'] = make_sure
        results['sv']['values']['close'] = dataframe['close'][-2]
        results['sv']['values']['high'] = dataframe['high'][-2]
        results['sv']['values']['low'] = dataframe['low'][-2]
        results['sv']['values']['ssl_up'] = ssl_channel['ssl_up'][-2]
        results['sv']['values']['ssl_up_pre'] = ssl_channel['ssl_up'][-3]
        results['sv']['values']['ssl_down'] = ssl_channel['ssl_down'][-2]
        results['sv']['values']['ssl_down_pre'] = ssl_channel['ssl_down'][-3]
        results['sv']['values']['spike'] =  vo['spike'][-2]
        results['sv']['values']['abs_line'] = vo['upper_line'][-2]

        #df_results = pandas.DataFrame(results)
        return results