"""
bitfxrequest - a simple client for the bitfinex REST API:
https://api-pub.bitfinex.com/v2/
which helps to get a list of symbols of such currencies
which have an exchange rate against the dollar through
the get_symbols() func., and also get the values of the
last CLOSE and average VOLUME for the last 10 days
via get_rate() func.
"""

import logging
import time
from datetime import datetime, timedelta

import requests

BASE_URL = "https://api-pub.bitfinex.com/v2/"


def get_symbols(usd_only=True):
    """
    Example of usage:

    get_symbols()

    Returns a list of symbols of such currencies
    which have an exchange rate against the dollar
    (default behavior)
    """
    res = requests.get("{}tickers?symbols=ALL".format(BASE_URL))
    assert "application/json" in res.headers.get("Content-Type", "")
    res = res.json()
    assert type(res) is list

    def ret():
        for i in res:
            cur = i[0]
            if len(cur) < 7:
                continue
            if usd_only and cur[-3:] != "USD":
                continue
            yield cur[1:4]

    return [i for i in ret()]


def get_candles(symbol, limit=10):
    """
    Example of usage:

    get_candles('BTC')

    Returns list of tuples like this for last 10 days by default:
    (
        datetime.datetime(2019, 10, 6, 4, 0),
        8038.2,        # CLOSE
        3629.81546451  # VOLUME
    )
    """
    res = requests.get(
        "{}candles/trade:1D:t{}USD/hist?limit={}".format(BASE_URL, symbol, limit)
    )
    assert "application/json" in res.headers.get("Content-Type", "")
    try:
        res = res.json()
        assert type(res) is list or dict
    except AssertionError:
        return None
    if res == []:
        return -1

    def get_time(millis):
        assert type(millis) is int
        return datetime.fromtimestamp(millis // 1000)

    def ret():
        for i in res:
            try:
                assert len(i) == 6
                t = get_time(i[0])
            except AssertionError:
                pass
            else:
                yield t, i[2], i[-1]

    return [i for i in ret()]


def get_rate(symbol, limit=10):
    """
    Example of usage:

    get_rate('BTC')

    Returns tuple like this:
    (
        'BTC',
        datetime.datetime(2019, 10, 6, 4, 0),
        8069.17377984,     # last value of CLOSE from get_candles() func.
        5282.882448599001  # average VOLUME for <limit> days
    )

    https://docs.bitfinex.com/reference#rest-public-candles
    """
    candles = get_candles(symbol, limit)
    if candles == -1:
        logging.warning("empty candles list")
        return (symbol, None, None, None)
    if type(candles) is dict:
        logging.warning("re-request required: {}".format(candles))
        return None
    try:
        assert len(candles) > 0
        assert len(candles[0]) > 1
        last_date = candles[0][0]
        last_rate = candles[0][1]
    except AssertionError:
        return None

    avg_days_count = limit
    exclude_date = datetime.now().date() - timedelta(days=avg_days_count)
    candles_in_limit_days = [i[-1] for i in candles if i[0].date() > exclude_date]

    def calc_average_volume():
        if candles_in_limit_days:
            return sum(candles_in_limit_days) / len(candles_in_limit_days)
        else:
            return 0

    return symbol, last_date, last_rate, calc_average_volume()


def get_rates():
    """
    Example of usage:

    list(get_rates())

    Returns generator of tuples with result from get_rate(symbol)
    for all available symbols from get_symbols() func.
    """
    symbols = get_symbols()
    for symbol in symbols:

        def try_get_rate(tries=10):
            """
            quote from https://docs.bitfinex.com/docs/rest-general
            NOTE
            In order to offer the best service possible we have added a rate limit to the number of REST requests.
            Our rate limit policy can vary in a range of 10 to 90 requests per minute depending on some factors (e.g. servers load, endpoint, etc.).
            """
            pause = 30
            while tries:
                rate = get_rate(symbol)
                if rate is None:
                    logging.warning(
                        "unsuccessful rate request for {}. sleeping: {} sec".format(
                            symbol, pause
                        )
                    )
                    time.sleep(pause)
                    pause *= 2
                    tries -= 1
                else:
                    return rate
            return None

        yield try_get_rate()


if __name__ == "__main__":

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(asctime)s]  %(message)s")

    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    for i in get_rates():
        print(i)
