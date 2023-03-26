import time

from logger import logger
import  config
import scan_signals
from notify import NotiFy
import multiprocessing
import math


def scan_pairs_queue(pairs):
    conf = config.Configure()
    configure = conf.get_config()
    scanner = scan_signals.SignalScaner(configure)
    scan_dict = scanner.config['scan']
    fmt_results = []
    for pair in pairs:
        for signal, peroid_list in scan_dict.items():
            for peroid in peroid_list:
                result = scanner.get_signal_result_with_peroid(pair, signal, peroid)
                #print("pair: %s signal: %s period:%s\n%s" % (pair, signal, peroid, result))
                if result['is_hot'] or result['is_cold']:
                    fmt_result = scanner._format_result(pair, peroid, signal, result)
                    fmt_results.append(fmt_result)
    return fmt_results

def err_call_back(err):
    print(f'error：{str(err)}')

if __name__=="__main__":

    conf = config.Configure()
    configure = conf.get_config()
    cpu_count = multiprocessing.cpu_count()
    cpu_use = math.ceil(cpu_count * 0.8)
    pair_list = configure['pairlists']
    length = len(pair_list)
    if length > 0:
        pairs_group = []
        i = 0
        for pair in pair_list:
            if len(pairs_group) < cpu_use:
                pairs = [pair]
                pairs_group.append(pairs)
            else:
                pairs_group[i % cpu_use].append(pair)
                i += 1

        while True:
            pool = multiprocessing.Pool(cpu_use)
            results = []
            for pairs in pairs_group:
                results.append(pool.apply_async(scan_pairs_queue, args=(pairs,),error_callback=err_call_back))
            pool.close()
            pool.join()


            print(f'results length：{str(len(results))}')
            for res in results:
                print(res.get())
        #if len(q) > 0:
        #    notifier.notify_all(results)