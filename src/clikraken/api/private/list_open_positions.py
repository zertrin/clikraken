# -*- coding: utf-8 -*-

"""
clikraken.api.private.list_open_positions

This module queries the OpenPositions method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import argparse
from datetime import datetime
from collections import OrderedDict

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import _tabulate as tabulate
from clikraken.clikraken_utils import csv
from clikraken.clikraken_utils import process_options


def list_open_positions(args):
    """List open positions."""
    args = process_options({}, {})
    return list_open_positions_api(args)


def list_open_positions_api(args):
    """List open positions."""

    # Parameters to pass to the API
    api_params = {
        "docalcs": "true",
    }

    res = query_api("private", "OpenPositions", api_params, args)

    return res


def list_open_positions_cmd(args):
    """List open positions."""
    res = list_open_positions_api(args)

    pos_list = []
    for order in res.values():
        pos = OrderedDict()
        pos["ordertxid"] = order["ordertxid"]
        pos["opening time"] = datetime.fromtimestamp(order["time"])
        pos["type"] = order["type"]
        pos["volume"] = order["vol"]
        pos["pair"] = order["pair"]
        pos["ordertype"] = order["ordertype"]
        pos["cost"] = order["cost"]
        pos["fee"] = order["fee"]
        pos["margin"] = order["margin"]
        pos["value"] = order["value"]
        pos["profit/loss"] = order["net"]
        pos["rollover time"] = datetime.fromtimestamp(int(order["rollovertm"]))
        pos["rollover terms"] = order["terms"]

        pos_list.append(pos)

    if args.csv:
        print(csv(pos_list, headers="keys"))
    else:
        print(tabulate(pos_list, headers="keys"))


def init(subparsers):
    parser_oplist = subparsers.add_parser(
        "positions",
        aliases=["pos"],
        help="[private] Get a list of your open positions",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_oplist.set_defaults(sub_func=list_open_positions_cmd)
