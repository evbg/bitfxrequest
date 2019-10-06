# -*- coding: utf-8 -*-
from bitfxrequest import get_symbols


def test_get_symbols_usd_only():
    symbols = get_symbols()
    assert len(symbols) > 0
    assert "USD" not in symbols
    for s in symbols:
        assert len(s) == 3
