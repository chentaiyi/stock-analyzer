import time

from logger import logger
import  config
import scan_signals
from notify import NotiFy

def main():

    try:
        conf = config.Configure()
        configure=conf.get_config()
        scanner = scan_signals.SignalScaner(configure)
        notifier = NotiFy(configure)
        while True:
            results = scanner.scan_all()
            if len(results) > 0:
                notifier.notify_all(results)
            time.sleep(2)
    except Exception as e:
        logger.outputlog(e)

if __name__ == '__main__':
    main()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
