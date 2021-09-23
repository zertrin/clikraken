# -*- coding: utf-8 -*-

"""
clikraken.api.public.asset_pairs

This module queries the AssetPairs method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import argparse
from collections import OrderedDict

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import _tabulate as tabulate
from clikraken.clikraken_utils import csv
from clikraken.clikraken_utils import process_options


def asset_pairs():
    """Get available asset pairs."""
    args = process_options({}, {})
    return asset_pairs_api(args)


def asset_pairs_api(args):
    """Get available asset pairs."""

    # Parameters to pass to the API
    api_params = {}

    res = query_api("public", "AssetPairs", api_params, args)

    return res


def asset_pairs_cmd(args):
    """Get available asset pairs."""

    res = asset_pairs_api(args)

    # initialize a list to store the parsed assets pairs
    assetlist = []

    for assetpair in res:
        if assetpair.endswith(".d"):
            continue
        ad = OrderedDict()
        ad["Pair"] = assetpair
        ad["Alt Name"] = res[assetpair]["altname"]
        ad["Base"] = res[assetpair]["base"]
        ad["Quote"] = res[assetpair]["quote"]
        assetlist.append(ad)

    if args.csv:
        print(csv(assetlist, headers="keys"))
    else:
        print(tabulate(assetlist, headers="keys"))
        print("--- Total: {} pairs".format(len(assetlist)))


def init(subparsers):
    parser_asset_pairs = subparsers.add_parser(
        "asset_pairs",
        aliases=["ap"],
        help="[public] Get the list of available asset pairs",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_asset_pairs.set_defaults(sub_func=asset_pairs_cmd)
