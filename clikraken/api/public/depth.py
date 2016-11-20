# -*- coding: utf8 -*-

"""
clikraken.api.public.depth

This module queries the Depth method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENCE file.
"""

from collections import OrderedDict
from decimal import Decimal

from tabulate import tabulate

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import asset_pair_short, print_results, humanize_timestamp


def depth(args):
    """Get market depth information."""

    # Parameters to pass to the API
    params = {
        'pair': args.pair,
        'count': args.count
    }

    res = query_api('public', 'Depth', params)

    if args.raw:
        print_results(res)

    res = res.get('result')
    if not res:
        return

    depth_dict = {'asks': [], 'bids': []}
    depth_label = {'asks': "Ask", 'bids': "Bid"}

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
        depth_dict[dtype] = reversed(sorted(depth_dict[dtype], key=lambda dentry: Decimal(dentry[price_label])))

    asks_table = tabulate(depth_dict['asks'], headers="keys")
    bids_table = tabulate(depth_dict['bids'], headers="keys")

    print("{}\n\n{}".format(asks_table, bids_table))
