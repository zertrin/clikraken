# -*- coding: utf-8 -*-

"""
clikraken.api.public.last_trades

This module queries the Trades method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import argparse
from collections import OrderedDict

import clikraken.global_vars as gv

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import (
    humanize_timestamp,
    base_quote_short_from_asset_pair,
)
from clikraken.clikraken_utils import _tabulate as tabulate
from clikraken.clikraken_utils import csv
from clikraken.clikraken_utils import process_options

pair_help = "asset pair"

OPTIONS = (
    (("-p", "--pair"), {"default": gv.DEFAULT_PAIR, "help": pair_help}),
    (("-s", "--since"), {"default": None, "help": "return trade data since given id"}),
    (
        ("-c", "--count"),
        {"type": int, "default": 15, "help": "maximum number of trades."},
    ),
)

MANDATORY_OPTIONS = ("pair",)


def last_trades(**kwargs):
    """Get last trades."""
    args = process_options(kwargs, OPTIONS, MANDATORY_OPTIONS)
    return last_trades_api(args)


def last_trades_api(args):
    """Get last trades."""

    # Parameters to pass to the API
    api_params = {
        "pair": args.pair,
    }
    if args.since:
        api_params["since"] = args.since

    res = query_api("public", "Trades", api_params, args)

    return res


def last_trades_cmd(args):
    """Get last trades."""
    res = last_trades_api(args)
    _, quote_currency = base_quote_short_from_asset_pair(args.pair)
    results = res[args.pair]
    last_id = res["last"]

    # initialize a list to store the parsed trades
    tlist = []

    # mappings
    ttype_label = {"b": "buy", "s": "sell"}
    otype_label = {"l": "limit", "m": "market"}

    for trade in results:
        # Initialize an OrderedDict to garantee the column order
        # for later use with the tabulate function
        tdict = OrderedDict()
        tdict["Trade type"] = ttype_label.get(trade[3], "unknown")
        tdict["Order type"] = otype_label.get(trade[4], "unknown")
        tdict["Price"] = trade[0]
        tdict["Volume"] = trade[1]
        tdict["Age"] = humanize_timestamp(trade[2])
        # tdict["Misc"] = trade[5]
        tlist.append(tdict)

    if not tlist:
        return

    # Reverse trade list to have the most recent trades at the top
    tlist = tlist[::-1]

    if args.csv:
        print(csv(tlist[: args.count], headers="keys"))
    else:
        print(tabulate(tlist[: args.count], headers="keys") + "\n")

        # separate the trades based on their type
        sell_trades = [x for x in tlist if x["Trade type"] == "sell"]
        buy_trades = [x for x in tlist if x["Trade type"] == "buy"]

        last_sell = sell_trades[0]
        last_buy = buy_trades[0]
        lt = [
            ["", "Price (" + quote_currency + ")", "Volume", "Age"],
            ["Last Sell", last_sell["Price"], last_sell["Volume"], last_sell["Age"]],
            ["Last Buy", last_buy["Price"], last_buy["Volume"], last_buy["Age"]],
        ]

        print(tabulate(lt, headers="firstrow") + "\n")

        print("Last ID = {}".format(last_id))


def init(subparsers):
    parser_last_trades = subparsers.add_parser(
        "last_trades",
        aliases=["lt"],
        help="[public] Get the last trades",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    for (args, kwargs) in OPTIONS:
        parser_last_trades.add_argument(*args, **kwargs)
    parser_last_trades.set_defaults(sub_func=last_trades_cmd)
