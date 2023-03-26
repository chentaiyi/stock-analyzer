

from Analysis.trading_signals import *


class SignalAnalyzer():
    """Contains all the methods required for analyzing strategies.
    """


    def signal_dispatcher(self):
        """Returns a dictionary for dynamic anaylsis selector
           trading signal dispatcher
           交易信号处理调度器
        """

        dispatcher = {
           'ma_nmacd_rsi':ma_nmacd_rsi.MaNmacdRsi().analyze,
            'hhc': hhc.HHC().analyze,
            'svc':ssl_vo_cmf.SslVoCmf().analyze,
            'sv':ssl_vo.SslVo().analyze,
            'mr':macd_rsi.MacdRsi().analyze,
        }
        return dispatcher




