# -*- coding: utf-8 -*-

"""
clikraken.api.private.get_balance

This module queries the Balance method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import argparse
from collections import OrderedDict
from decimal import Decimal

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import _tabulate as tabulate
from clikraken.clikraken_utils import csv
from clikraken.clikraken_utils import process_options


def get_balance():
    """Get user balance function to use in python scripts."""
    args = process_options({}, {})
    res = get_balance_api(args)
    copy = {}
    for asset in res:
        val = Decimal(res[asset])
        if len(asset) == 4 and asset[0] in ["Z", "X"]:
            copy[asset[1:]] = val
        else:
            copy[asset] = val
    return copy


def get_balance_api(args):
    """Get user balance API call."""
    res = query_api("private", "Balance", {}, args)
    return res


def get_balance_cmd(args=None):
    """Get user balance CLI cmd."""

    res = get_balance_api(args)

    bal_list = []
    for asset in res:
        # Initialize an OrderedDict to garantee the column order
        # for later use with the tabulate function
        asset_dict = OrderedDict()
        # Remove leading Z or X from asset pair if it is of length 4
        asset_dict["asset"] = (
            asset[1:] if len(asset) == 4 and asset[0] in ["Z", "X"] else asset
        )
        asset_dict["balance"] = res[asset]
        bal_list.append(asset_dict)

    if not bal_list:
        return

    # Sort alphabetically
    bal_list = sorted(bal_list, key=lambda asset_dict: asset_dict["asset"])

    if args.csv:
        print(csv(bal_list, headers="keys"))
    else:
        print(tabulate(bal_list, headers="keys"))


def init(subparsers):
    parser_balance = subparsers.add_parser(
        "balance",
        aliases=["bal"],
        help="[private] Get your current balance",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_balance.set_defaults(sub_func=get_balance_cmd)
