# -*- coding: utf-8 -*-

"""
clikraken.api.public.ticker

This module queries the Ticker method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import argparse
from collections import OrderedDict
from decimal import Decimal

import clikraken.global_vars as gv

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import _tabulate as tabulate
from clikraken.clikraken_utils import asset_pair_short
from clikraken.clikraken_utils import csv
from clikraken.clikraken_utils import process_options

pairs_help = "comma delimited list of asset pairs"

OPTIONS = (
    (
        ("-p", "--pair"),
        {"default": gv.TICKER_PAIRS, "help": pairs_help + " to get info on. "},
    ),
)

MANDATORY_OPTIONS = ("pair",)


def ticker(**kwargs):
    """Get currency ticker information."""
    args = process_options(kwargs, OPTIONS, MANDATORY_OPTIONS)
    return ticker_api(args)


def ticker_api(args):
    """Get currency ticker information."""

    # Parameters to pass to the API
    api_params = {
        "pair": args.pair,
    }

    res = query_api("public", "Ticker", api_params, args)

    return res


def ticker_cmd(args):
    """Get currency ticker information."""
    res = ticker_api(args)
    # the list will contain one OrderedDict containing
    # the parser ticker info per asset pair
    ticker_list = []

    for pair in res:
        # extract the results for the current pair
        pair_res = res[pair]

        # Initialize an OrderedDict to garantee the column order
        # for later use with the tabulate function
        pticker = OrderedDict()

        pticker["pair"] = asset_pair_short(pair)
        pticker["last"] = pair_res["c"][0]  # price only
        pticker["high"] = pair_res["h"][1]  # last 24h
        pticker["low"] = pair_res["l"][1]  # last 24h
        pticker["vol"] = pair_res["v"][1]  # last 24h
        pticker["wavg"] = pair_res["p"][1]  # last 24h

        # calculate an estimate of the traded volume in quoted currency
        # for the last 24h: Volume x Average price
        quote_val = Decimal(pticker["vol"]) * Decimal(pticker["wavg"])

        unit_prefix = ""
        if quote_val >= 10e6:
            quote_val = quote_val / Decimal(1e6)
            unit_prefix = "M"
        elif quote_val >= 10e3:
            quote_val = quote_val / Decimal(1e3)
            unit_prefix = "k"

        pticker["vol value"] = (
            str(round(quote_val)) + " " + unit_prefix + pticker["pair"][-3:]
        )

        # get the price only
        pticker["ask"] = pair_res["a"][0]
        pticker["bid"] = pair_res["b"][0]

        ticker_list.append(pticker)

    if not ticker_list:
        return

    ticker_list = sorted(ticker_list, key=lambda pticker: pticker["pair"])

    if args.csv:
        print(csv(ticker_list, headers="keys"))
    else:
        print(tabulate(ticker_list, headers="keys"))


def init(subparsers):
    parser_ticker = subparsers.add_parser(
        "ticker",
        aliases=["t"],
        help="[public] Get the ticker",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    for (args, kwargs) in OPTIONS:
        parser_ticker.add_argument(*args, **kwargs)
    parser_ticker.set_defaults(sub_func=ticker_cmd)
