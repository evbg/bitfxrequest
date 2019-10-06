from datetime import datetime
from bitfxrequest import get_rates


def test_get_rates_01():
    rates = zip(range(3), get_rates())
    for n, rate in rates:
        assert len(rate) == 4
        assert type(rate[1]) is datetime
        assert type(rate[2]) is float
        assert type(rate[3]) is float
