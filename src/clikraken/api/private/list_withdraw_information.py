# -*- coding: utf-8 -*-

"""
clikraken.api.private.list_withdraw_information

This module queries the WithdrawInfo method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import argparse
from decimal import Decimal

import clikraken.global_vars as gv

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import _tabulate as tabulate
from clikraken.clikraken_utils import csv
from clikraken.clikraken_utils import process_options

OPTIONS = (
    (("-a", "--asset"), {"default": gv.DEFAULT_ASSET, "help": "asset to list"}),
    (("amount",), {"type": Decimal, "help": "Amount to be withdrawn"}),
    (("key",), {"type": str, "help": "Withdrawal key name, as set up on the account"}),
)

MANDATORY_OPTIONS = ("asset", "amount", "key")


def list_withdraw_information(**kwargs):
    """List withdrawals."""
    args = process_options(kwargs, OPTIONS, MANDATORY_OPTIONS)

    return list_withdraw_information_api(args)


def list_withdraw_information_api(args):
    """List withdrawals."""

    # Parameters to pass to the API
    api_params = {
        "asset": args.asset,
        "amount": args.amount,
        "key": args.key,
    }

    res = query_api("private", "WithdrawInfo", api_params, args)

    return res


def list_withdraw_information_cmd(args):
    """List withdrawals."""

    res = {key: [value] for (key, value) in list_withdraw_information_api(args).items()}

    if args.csv:
        print(csv(res, headers="keys"))
    else:
        print(tabulate(res, headers="keys"))


def init(subparsers):
    parser_list_withdrawal = subparsers.add_parser(
        "list_withdraw_information",
        aliases=["lwi"],
        help="[private] List withdraw information",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    for (args, kwargs) in OPTIONS:
        parser_list_withdrawal.add_argument(*args, **kwargs)
    parser_list_withdrawal.set_defaults(sub_func=list_withdraw_information_cmd)
