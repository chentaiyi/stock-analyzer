

from logger import logger
from Notifiers.email_notifier import EmailNotifier

import config



class NotiFy():

    def __init__(self,conf):
        self.config = conf
        email_conf = self.config['notify']['email']
        self.email_notifer = EmailNotifier(email_conf)
        last_status = {}
        pairlists = self.config['pairlists']
        scan_signals = self.config['scan']
        for pair in pairlists:
            last_status[pair] = {}
            for signal in scan_signals:
                last_status[pair][signal] = {}
                for period in scan_signals[signal]:
                    last_status[pair][signal][period]='neutral'
        self.last_status = last_status

    def notify_all(self,content):
        filtered_results = self._filter_content(content)
        if len(filtered_results) > 0:
            self.email_notifer.notify(filtered_results)

    # 过滤与前次相同状态的信号以保证相同状态信号只通知一次
    def _filter_content(self, content):
        filtered_results = []
        for res in content:
            pair = res['pair']
            signal = res['signal']
            period = res['period']
            if self.last_status[pair][signal][period] != res['direction']:
                filtered_results.append(res)
                logger.outputlog(res)
                self.last_status[pair][signal][period] = res['direction']

        return filtered_results

