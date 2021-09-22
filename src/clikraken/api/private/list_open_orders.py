# -*- coding: utf-8 -*-

"""
clikraken.api.private.list_open_orders

This module queries the OpenOrders method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import argparse
from collections import namedtuple
from decimal import Decimal

from clikraken.api.api_utils import parse_order_res, query_api
from clikraken.clikraken_utils import asset_pair_short
from clikraken.clikraken_utils import _tabulate as tabulate
from clikraken.clikraken_utils import csv


def list_open_orders(txid=None):
    """List open orders."""
    Args = namedtuple(
        "Args",
        [
            "debug",
            "raw",
            "json",
            "csv",
            "txid",
        ],
    )
    args = Args(
        False,
        False,
        False,
        False,
        txid=txid,
    )
    return list_open_orders_api(args)


def list_open_orders_api(args):
    """List open orders."""

    # Parameters to pass to the API
    api_params = {
        # TODO
    }
    if args.txid:
        api_params.update({"txid": args.txid})
        res_ol = query_api("private", "QueryOrders", api_params, args)
    else:
        res = query_api("private", "OpenOrders", api_params, args)
        # extract list of orders from API results
        res_ol = res["open"]

    # the parsing is done in an helper function
    ol = parse_order_res(res_ol, ["open"])

    # filter and sort orders by price in each category
    for otype in ol:
        # filter orders based on currency pair
        if "pair" in args and args.pair:
            ol[otype] = [
                odict
                for odict in ol[otype]
                if (
                    odict["pair"] in [args.pair, asset_pair_short(args.pair)]
                    or args.pair == "all"
                )
            ]
        # sort orders by price
        ol[otype] = sorted(ol[otype], key=lambda odict: Decimal(odict["price"]))

    # final list is concatenation of buy orders followed by sell orders
    ol_all = ol["buy"] + ol["sell"]
    return ol_all


def list_open_orders_cmd(args):
    """List open orders."""
    ol_all = list_open_orders_api(args)

    if not ol_all:
        return

    if args.csv:
        print(csv(ol_all, headers="keys"))
    else:
        print(tabulate(ol_all, headers="keys"))


def init(subparsers):
    pair_help = "asset pair"
    parser_olist = subparsers.add_parser(
        "olist",
        aliases=["ol"],
        help="[private] Get a list of your open orders",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_olist.add_argument("-p", "--pair", default=None, help=pair_help)
    parser_olist.add_argument(
        "-i",
        "--txid",
        default=None,
        help="comma delimited list of transaction ids to query info about (20 maximum)",
    )
    parser_olist.set_defaults(sub_func=list_open_orders_cmd)
