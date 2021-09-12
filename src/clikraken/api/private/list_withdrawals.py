# -*- coding: utf-8 -*-

"""
clikraken.api.private.list_open_orders

This module queries the OpenOrders method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import argparse

import clikraken.global_vars as gv

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import _tabulate as tabulate
from clikraken.clikraken_utils import csv


def list_withdrawals(args):
    """List withdrawals."""

    # Parameters to pass to the API
    api_params = {"asset": args.asset}

    res = query_api("private", "WithdrawStatus", api_params, args)

    if args.csv:
        print(csv(res, headers="keys"))
    else:
        print(tabulate(res, headers="keys"))


def init(subparsers):
    parser_list_withdrawal = subparsers.add_parser(
        "list_withdrawals",
        aliases=["lw"],
        help="[private] List withdrawals",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_list_withdrawal.add_argument(
        "-a", "--asset", default=gv.DEFAULT_ASSET, help="asset to list"
    )
    parser_list_withdrawal.set_defaults(sub_func=list_withdrawals)
