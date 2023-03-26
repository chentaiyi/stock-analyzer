import pandas
import datetime
import re

import config
import analysis
import multiprocessing
import exchange
import math


class SignalScaner():
    '''
        scan signals
    '''

    def __init__(self, conf):
        self.config = conf
        if self.config is None:
            configure = config.Configure()
            self.config = configure.get_config()
        self.signal_analyzer = analysis.SignalAnalyzer()
        self.exchange_interface = exchange.ExchangeInterface()

    def scan_all(self):
        '''
        扫描所有监控标的的指标
        :return: 扫描结果数据
        '''
        pair_list = self.config['pairlists']
        scan_dict = self.config['scan']
        results = []
        for pair in pair_list:
            for signal, peroid_list in scan_dict.items():
                for peroid in peroid_list:
                    result = self.get_signal_result_with_peroid(pair, signal, peroid)
                    print("pair: %s signal: %s period:%s\n%s"%(pair,signal,peroid,result))
                    if result['is_hot'] or result['is_cold']:
                        fmt_result=self._format_result(pair,peroid,signal,result)
                        results.append(fmt_result)
        return results



    def scan_pairs(self,pairs,signals,peroids):
        results = []
        for pair in pairs:
            for signal in signals:
                for peroid in peroids:
                    result = self.get_signal_result_with_peroid(pair, signal, peroid)
                    print("pair: %s signal: %s period:%s\n%s"%(pair,signal,peroid,result))
                    if result['is_hot'] or result['is_cold']:
                        fmt_result = self._format_result(pair,peroid,signal,result)
                        results.append(fmt_result)
        return results

    def _format_result(self, pair, period, signal,analysis_result):
        result = {}
        result['pair'] = pair
        result['period'] = period
        result['signal'] = signal
        if analysis_result['is_hot']:
            result['direction'] = 'long'
        if analysis_result['is_cold']:
            result['direction'] = 'short'
        if self.config['signals'][signal]['show_details']:
            result['analysis'] = analysis_result
        return result


    def get_historical_data(self, market_pair, candle_period):
        """Gets a list of OHLCV data for the given pair and exchange.

        Args:
            market_pair (str): The market pair to get the OHLCV data for.
            exchange (str): The exchange to get the OHLCV data for.
            candle_period (str): The timeperiod to collect for the given pair and exchange.

        Returns:
            list: A list of OHLCV data.
        """

        historical_data = None
        try:
            historical_data = self.exchange_interface.get_historical_data(
                market_pair,
                candle_period
            )
        except Exception as err:
            print(err)
        return historical_data

    def get_signal_result_with_peroid(self, market_pair, signal, peroid):
        '''
        :param market_pair: 交易对
        :param signal: 信号
        :param peroid: 周期
        :return: result: 结果 dict
        '''
        signal_dispatcher = self.signal_analyzer.signal_dispatcher()
        result = {}
        if signal in self.config['signals'].keys() and self.config['signals'][signal]['enable']:
            peroid = peroid
            historical_data_cache = self.get_historical_data(market_pair, peroid)
            dispatcher_args = {'historical_data': historical_data_cache}
            try:
                result = signal_dispatcher[signal](**dispatcher_args)
            except Exception as err:
                print(err)

        return result

    def passed_delta_seconds(self, candle_period):
        '''
        当前时间超过上个周期的秒数
        eg.当前时间2022.10.25.8：01：25.周期为1小时
        则 passed_delta = 85(60+25)
        return: (passed_delta,delta)
        其中passed_delta 是当前超过上个周期的描述，delta为到下个周期剩余的秒数
        '''
        total_seconds = 0
        timeframe_regex = re.compile('([0-9]+)([a-zA-Z])')
        timeframe_matches = timeframe_regex.match(candle_period)
        time_quantity = timeframe_matches.group(1)
        time_period = timeframe_matches.group(2)
        next_time = self.get_next_peroid_time(time_unit=candle_period)
        delta = next_time - datetime.datetime.now()
        if time_period == 'h':
            total_seconds = int(time_quantity) * 3600
        elif time_period == 'm':
            total_seconds = int(time_quantity) * 60
        elif time_period == 'd':
            total_seconds = int(time_quantity) * 86400

        passed_delta = total_seconds - int(delta.seconds)
        return (passed_delta, int(delta.seconds))

        # 取下一个时间周期起始时间的datetime 支持d,能被24整除的H，以及能被60整除的m

    def get_next_peroid_time(self, time_unit):
        now = datetime.datetime.now()
        result = now
        print('nowis %s' % result)
        f = "%Y-%m-%d %H:%M:%S"
        timeframe_regex = re.compile('([0-9]+)([a-zA-Z])')
        timeframe_matches = timeframe_regex.match(time_unit)
        time_quantity = int(timeframe_matches.group(1))
        time_period = timeframe_matches.group(2)
        if time_period == 'h':
            if time_quantity > 0 and 24 % time_quantity == 0:
                start_time = now.date()
                end_time = start_time + pandas.Timedelta(1, unit='d')
                dindex = pandas.date_range(start=start_time, end=end_time, freq=time_unit)
                period_array = dindex.array
                i = 0
                while i < len(period_array) - 1:
                    if now > period_array[i] and now <= period_array[i + 1]:
                        result = period_array[i + 1]
                        break
                    i += 1
            else:
                print('The timeunit is not support!')
        if time_period == 'd':
            d = (now + datetime.timedelta(days=int(time_quantity))).strftime("%Y-%m-%d") + " 00:00:00"
            result = datetime.datetime.strptime(d, f)

        if time_period == 'm':
            if time_quantity > 0 and 60 % time_quantity == 0:
                now_h = now.strftime("%Y-%m-%d %H") + ":00:00"
                start_time = datetime.datetime.strptime(now_h, f)
                end_time = start_time + pandas.Timedelta(1, unit='h')
                freq = str(time_quantity) + 't'
                dindex = pandas.date_range(start=start_time, end=end_time, freq=freq)
                period_array = dindex.array
                i = 0
                while i < len(period_array) - 1:
                    if now > period_array[i] and now <= period_array[i + 1]:
                        result = period_array[i + 1]
                        break
                    i += 1
            else:
                print('The timeunit is not support!')
        print('next_time is %s' % result)
        return result



    def scan_pairs_queue(self,pairs,q):
        scan_dict= self.config['scan']
        for pair in pairs:
            for signal, peroid_list in scan_dict.items():
                for peroid in peroid_list:
                    result = scanner.get_signal_result_with_peroid(pair, signal, peroid)
                    print("pair: %s signal: %s period:%s\n%s" % (pair, signal, peroid, result))
                    if result['is_hot'] or result['is_cold']:
                        fmt_result = scanner._format_result(pair, peroid, signal, result)
                        q.put(fmt_result)

if __name__ == '__main__':
    conf = config.Configure()
    configure = conf.get_config()
    scanner = SignalScaner(configure)
    #start = datetime.datetime.now()
    #r = scanner.scan_all()
    #end = datetime.datetime.now()

    r= scanner.scan_pairs(scanner.config['pairlists'],['mr'],['1d'])
    print(r)



