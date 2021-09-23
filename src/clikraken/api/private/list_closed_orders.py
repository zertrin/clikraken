# -*- coding: utf-8 -*-

"""
clikraken.api.private.list_list_closed_orders

This module queries the ClosedOrders method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import argparse
from decimal import Decimal

from clikraken.api.api_utils import parse_order_res, query_api
from clikraken.clikraken_utils import asset_pair_short
from clikraken.clikraken_utils import _tabulate as tabulate
from clikraken.clikraken_utils import csv
from clikraken.clikraken_utils import process_options


pair_help = "asset pair"

OPTIONS = (
    (("-p", "--pair"), {"default": None, "help": pair_help}),
    (
        ("-i", "--txid"),
        {
            "default": None,
            "help": "comma delimited list of transaction ids to query info about (20 maximum)",
        },
    ),
)


def list_closed_orders(**kwargs):
    """List closed orders."""
    args = process_options(kwargs, OPTIONS)
    return list_closed_orders_api(args)


def list_closed_orders_api(args):
    """List closed orders."""

    # Parameters to pass to the API
    api_params = {
        # TODO
    }
    if args.txid:
        api_params.update({"txid": args.txid})
        res_ol = query_api("private", "QueryOrders", api_params, args)
    else:
        res = query_api("private", "ClosedOrders", api_params, args)
        # extract list of orders from API results
        res_ol = res["closed"]

    return res_ol


def list_closed_orders_cmd(args):
    """List closed orders."""
    res_ol = list_closed_orders_api(args)

    # the parsing is done in an helper function
    ol = parse_order_res(res_ol, ["closed", "canceled"])

    # merge order types in one list
    ol = ol["buy"] + ol["sell"]

    # filter out orders with zero volume executed
    ol = [odict for odict in ol if Decimal(odict["vol_exec"]) > 0]
    if "pair" in args and args.pair:
        ol = [
            odict
            for odict in ol
            if odict["pair"] in [args.pair, asset_pair_short(args.pair)]
        ]

    if not ol:
        return

    # sort by date
    ol = sorted(ol, key=lambda odict: odict["closing_date"])

    if args.csv:
        print(csv(ol, headers="keys"))
    else:
        print(tabulate(ol, headers="keys"))


def init(subparsers):
    parser_clist = subparsers.add_parser(
        "clist",
        aliases=["cl"],
        help="[private] Get a list of your closed orders",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    for (args, kwargs) in OPTIONS:
        parser_clist.add_argument(*args, **kwargs)
    parser_clist.set_defaults(sub_func=list_closed_orders_cmd)
