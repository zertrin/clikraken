# -*- coding: utf8 -*-

"""
clikraken.api.private.get_trade_balance

This module queries the TradeBalance method of Kraken's API
and outputs the results.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import _tabulate as tabulate


def get_trade_balance(args=None):
    """Get user trade balance."""

    # Parameters to pass to the API
    api_params = {}

    res = query_api('private', 'TradeBalance', api_params, args)

    tb_fields = {
        'eb': 'equivalent balance',
        'tb': 'trade balance',
        'm': 'margin amount of open positions',
        'n': 'unrealized net profit/loss of open positions',
        'c': 'cost basis of open positions',
        'v': 'current floating valuation of open positions',
        'e': 'equity',
        'mf': 'free margin',
        'ml': 'margin level',
    }

    tbal_list = []
    for k in res:
        if k in tb_fields:
            tbal_list.append([tb_fields[k], res[k]])
    print(tabulate(tbal_list))
