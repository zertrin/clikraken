# -*- coding: utf-8 -*-

"""
clikraken.api.public.depth

This module queries the Depth method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import argparse
from collections import OrderedDict
from decimal import Decimal

import clikraken.global_vars as gv

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import asset_pair_short, humanize_timestamp
from clikraken.clikraken_utils import _tabulate as tabulate
from clikraken.clikraken_utils import csv


def depth(args):
    """Get market depth information."""

    # Parameters to pass to the API
    api_params = {"pair": args.pair, "count": args.count}

    res = query_api("public", "Depth", api_params, args)

    depth_dict = {"asks": [], "bids": []}
    depth_label = {"asks": "Ask", "bids": "Bid"}

    shortpair = asset_pair_short(args.pair)

    # dtype is 'asks' or 'bids'
    for dtype in depth_dict:
        # extract the array of market depth from the api results
        dlist = res[args.pair][dtype]
        # build a column label depending on the asset pair and dtype
        price_label = shortpair + " " + depth_label[dtype]

        for delem in dlist:
            # Initialize an OrderedDict to garantee the column order
            # for later use with the tabulate function
            dentry = OrderedDict()
            dentry[price_label] = delem[0]
            dentry["Volume"] = delem[1]
            dentry["Age"] = humanize_timestamp(delem[2])
            depth_dict[dtype].append(dentry)

        if not dlist:
            continue

        # sort by price descending
        depth_dict[dtype] = reversed(
            sorted(depth_dict[dtype], key=lambda dentry: Decimal(dentry[price_label]))
        )

    if args.csv:
        output = []
        for dtype in depth_dict.keys():
            for o in depth_dict[dtype]:
                it = OrderedDict()
                it["dtype"] = dtype
                for k, v in o.items():
                    if len(k.split(" ")) > 1:
                        # key has a space, this is the "price_label" column -> "XABCZDEF Ask"
                        it["pair"] = k.split(" ")[0]  # keep only "XABCZDEF"
                        it["price"] = v
                    else:
                        # the other columns don't contain a space
                        it[k] = v
                output += [it]
        print(csv(output, headers="keys"))
    else:
        asks_table = tabulate(depth_dict["asks"], headers="keys")
        bids_table = tabulate(depth_dict["bids"], headers="keys")
        print("{}\n\n{}".format(asks_table, bids_table))


def init(subparsers):
    pair_help = "asset pair"
    parser_depth = subparsers.add_parser(
        "depth",
        aliases=["d"],
        help="[public] Get the current market depth data",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_depth.add_argument("-p", "--pair", default=gv.DEFAULT_PAIR, help=pair_help)
    parser_depth.add_argument(
        "-c", "--count", type=int, default=7, help="maximum number of asks/bids."
    )
    parser_depth.set_defaults(sub_func=depth)
