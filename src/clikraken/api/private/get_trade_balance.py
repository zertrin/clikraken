# -*- coding: utf-8 -*-

"""
clikraken.api.private.get_trade_balance

This module queries the TradeBalance method of Kraken's API
and outputs the results.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import argparse

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import _tabulate as tabulate
from clikraken.clikraken_utils import csv
from clikraken.clikraken_utils import process_options


def get_trade_balance(**kwargs):
    """Get user trade balance."""
    args = process_options({}, {})
    return get_trade_balance_api(args)


def get_trade_balance_api(args=None):
    """Get user trade balance."""

    # Parameters to pass to the API
    api_params = {}

    res = query_api("private", "TradeBalance", api_params, args)

    return res


def get_trade_balance_cmd(args=None):
    """Get user trade balance."""
    res = get_trade_balance_api(args)
    tbal_list = [
        ["equivalent balance", res.get("eb", "n/a")],
        ["trade balance", res.get("tb", "n/a")],
        ["margin amount of open positions", res.get("m", "n/a")],
        ["cost basis of open positions", res.get("c", "n/a")],
        ["current floating valuation of open positions", res.get("v", "n/a")],
        ["equity", res.get("e", "n/a")],
        ["free margin", res.get("mf", "n/a")],
        ["margin level", res.get("ml", "n/a")],
        ["unrealized net profit/loss of open positions", res.get("n", "n/a")],
    ]
    if args.csv:
        d = [{key: value for key, value in tbal_list}]
        k = [key for key, value in tbal_list]
        print(csv(d, headers=k))
    else:
        print(tabulate(tbal_list))


def init(subparsers):
    parser_trade_balance = subparsers.add_parser(
        "trade_balance",
        aliases=["tbal"],
        help="[private] Get your current trade balance",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_trade_balance.set_defaults(sub_func=get_trade_balance_cmd)
