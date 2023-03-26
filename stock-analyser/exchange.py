
from tenacity import retry, retry_if_exception_type, stop_after_attempt
from Ashare import *


class ExchangeInterface():
    """Interface for performing queries against exchange API's
    """

    @retry(retry=retry_if_exception_type(Exception), stop=stop_after_attempt(3))
    def get_historical_data(self, market_pair, time_unit, start_date='', max_periods=300):
        """Get historical OHLCV for a symbol pair

        Decorators:
            retry

        Args:
            market_pair (str): Contains the symbol pair to operate on i.e. sh000001 or 600519.XSHG(茅台）
            exchange (str): Contains the exchange to fetch the historical data from.
            time_unit (str): A string specifying the time unit i.e. 5m or 1d.
            start_date (str, optional): start time unit.
            max_periods (int, optional): Defaults to 300. Maximum number of time periods
              back to fetch data for.

        Returns:
            list: Contains a list of lists which contain timestamp, open, high, low, close, volume.
        """
        historical_data = None

        try:
            historical_data = get_price(code=market_pair,end_date=start_date,frequency=time_unit,count=max_periods)
        except Exception as e:
            print(e)

        return historical_data



if __name__ == "__main__":

    pass
