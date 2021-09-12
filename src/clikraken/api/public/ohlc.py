# -*- coding: utf-8 -*-

"""
clikraken.api.public.ohlc

This module queries the OHLC method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import argparse
from collections import OrderedDict

import clikraken.global_vars as gv

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import format_timestamp, asset_pair_short
from clikraken.clikraken_utils import _tabulate as tabulate
from clikraken.clikraken_utils import csv


def ohlc(args):
    """Get OHLC data for asset pairs for various minute intervals:
    1 (default), 5, 15, 30, 60, 240, 1440, 10800, 21600."""

    # Parameters to pass to the API
    api_params = {
        "pair": args.pair,
    }
    if args.since:
        api_params["since"] = args.since

    if args.interval:
        api_params["interval"] = interval = args.interval
    else:
        interval = 1

    res = query_api("public", "OHLC", api_params, args)

    results = res[args.pair]
    last_id = res["last"]

    # initialize a list to store the parsed ohlc data
    ohlclist = []

    for period in results:
        # Initialize an OrderedDict to garantee the column order
        # for later use with the tabulate function
        ohlcdict = OrderedDict()
        ohlcdict["Time"] = format_timestamp(period[0])
        ohlcdict["Open"] = period[1]
        ohlcdict["High"] = period[2]
        ohlcdict["Low"] = period[3]
        ohlcdict["Close"] = period[4]
        ohlcdict["VWAP"] = period[5]
        ohlcdict["Volume"] = period[6]
        ohlcdict["Count"] = period[7]
        ohlclist.append(ohlcdict)

    if not ohlclist:
        return

    # Reverse trade list to have the most recent interval at the top
    ohlclist = ohlclist[::-1]

    if args.csv:
        print(csv(ohlclist[: args.count], headers="keys"))
    else:
        print("Asset pair: " + asset_pair_short(args.pair))
        print("Interval: " + str(interval) + "m\n")

        print(tabulate(ohlclist[: args.count], headers="keys") + "\n")

        print("Last ID = {}".format(last_id))


def init(subparsers):
    pair_help = "asset pair"
    parser_ohlc = subparsers.add_parser(
        "ohlc",
        aliases=["oh"],
        help="[public] Get the ohlc data",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_ohlc.add_argument("-p", "--pair", default=gv.DEFAULT_PAIR, help=pair_help)
    parser_ohlc.add_argument(
        "-i",
        "--interval",
        default=1,
        help="return ohlc data for interval in minutes; 1, 5, 15, 30, 60, 240, 1440, 10800, 21600.",
    )
    parser_ohlc.add_argument(
        "-s", "--since", default=None, help="return ohlc data since given id"
    )
    parser_ohlc.add_argument(
        "-c", "--count", type=int, default=50, help="maximum number of intervals."
    )
    parser_ohlc.set_defaults(sub_func=ohlc)
