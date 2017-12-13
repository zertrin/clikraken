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
        ['equivalent balance', res.get('eb', 'n/a')],
        ['trade balance', res.get('tb', 'n/a')],
        ['margin amount of open positions', res.get('m', 'n/a')],
        ['cost basis of open positions', res.get('c', 'n/a')],
        ['current floating valuation of open positions', res.get('v', 'n/a')],
        ['equity', res.get('e', 'n/a')],
        ['free margin', res.get('mf', 'n/a')],
        ['margin level', res.get('ml', 'n/a')],
        ['unrealized net profit/loss of open positions', res.get('n', 'n/a')],
    ]
    print(tabulate(tbal_list))
