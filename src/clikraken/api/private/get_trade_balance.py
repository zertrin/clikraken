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

    tbal_list = [
        ['equivalent balance', res['eb']],
        ['trade balance', res['tb']],
        ['margin amount of open positions', res['m']],
        ['cost basis of open positions', res['c']],
        ['current floating valuation of open positions', res['v']],
        ['equity', res['e']],
        ['free margin', res['mf']],
        ['margin level', res['ml']],
        ['unrealized net profit/loss of open positions', res['n']],
    ]
    print(tabulate(tbal_list))
