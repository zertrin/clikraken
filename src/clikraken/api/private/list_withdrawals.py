# -*- coding: utf-8 -*-

"""
clikraken.api.private.list_withdrawals

This module queries the WithdrawStatus method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import argparse

import clikraken.global_vars as gv

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import _tabulate as tabulate
from clikraken.clikraken_utils import csv
from clikraken.clikraken_utils import process_options

OPTIONS = ((("-a", "--asset"), {"default": gv.DEFAULT_ASSET, "help": "asset to list"}),)

MANDATORY_OPTIONS = ("asset",)


def list_withdrawals(**kwargs):
    """List withdrawals."""

    args = process_options(kwargs, OPTIONS, MANDATORY_OPTIONS)

    return list_withdrawals_api(args)


def list_withdrawals_api(args):
    """List withdrawals."""

    # Parameters to pass to the API
    api_params = {"asset": args.asset}

    res = query_api("private", "WithdrawStatus", api_params, args)
    return res


def list_withdrawals_cmd(args):
    """List withdrawals."""

    res = list_withdrawals_api(args)
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
    for (args, kwargs) in OPTIONS:
        parser_list_withdrawal.add_argument(*args, **kwargs)
    parser_list_withdrawal.set_defaults(sub_func=list_withdrawals_cmd)
