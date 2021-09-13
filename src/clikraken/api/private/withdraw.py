# -*- coding: utf-8 -*-

"""
clikraken.api.private.withdraw

This module queries the Withdraw method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import argparse
from decimal import Decimal

import clikraken.global_vars as gv
from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import _tabulate as tabulate
from clikraken.clikraken_utils import csv


def withdraw(args):
    """Withdraw an asset."""

    # Parameters to pass to the API
    api_params = {
        "asset": args.asset,
        "amount": args.amount,
        "key": args.key,
    }

    res = query_api("private", "Withdraw", api_params, args)

    if args.csv:
        print(csv(res, headers="keys"))
    else:
        print(tabulate(res, headers="keys"))


def init(subparsers):
    parser_withdraw = subparsers.add_parser(
        "withdraw",
        aliases=["wd"],
        help="[private] Withdraw funds.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_withdraw.add_argument(
        "-a", "--asset", default=gv.DEFAULT_ASSET, help="asset being withdrawn"
    )
    parser_withdraw.add_argument("amount", type=Decimal, help="Amount to be withdrawn")
    parser_withdraw.add_argument(
        "key", type=str, help="Withdrawal key name, as set up on the account"
    )
    parser_withdraw.set_defaults(sub_func=withdraw)
