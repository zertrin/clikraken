# -*- coding: utf-8 -*-

"""
clikraken.api.private.get_deposit_addresses

This module queries the DepositAddresses method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import argparse
from collections import OrderedDict

import clikraken.global_vars as gv
from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import csv, format_timestamp
from clikraken.clikraken_utils import _tabulate as tabulate
from clikraken.clikraken_utils import process_options

OPTIONS = (
    (("-a", "--asset"), {"default": gv.DEFAULT_ASSET, "help": "asset being deposited"}),
    (("-m", "--method"), {"default": None, "help": "name of the deposit method"}),
    (
        ("-n", "--new"),
        {"action": "store_true", "help": "whether or not to generate a new address"},
    ),
    (("-1", "--one"), {"action": "store_true", "help": "return just one address"}),
)

MANDATORY_OPTIONS = ("asset",)


def get_deposit_addresses(**kwargs):
    """Get deposit addresses."""
    args = process_options(kwargs, OPTIONS, MANDATORY_OPTIONS)

    return get_deposit_addresses_api(args)


def get_deposit_addresses_api(args):
    """Get deposit addresses."""

    # Parameters to pass to the API
    api_params = {
        "asset": args.asset,
        "method": args.method,
    }
    if args.new:
        api_params["new"] = args.new

    res = query_api("private", "DepositAddresses", api_params, args)

    return res


def get_deposit_addresses_cmd(args):
    """Get deposit addresses."""

    res = get_deposit_addresses_api(args)
    if not res:
        return

    if args.one:
        # Get preferably not used addresses
        addresses = [a for a in res if a.get("new", False)] or res
        print(addresses[0]["address"])
        return

    addresses_list = []
    for address in res:
        # Initialize an OrderedDict to garantee the column order
        # for later use with the tabulate function
        asset_dict = OrderedDict()
        # Remove leading Z or X from asset pair if it is of length 4
        asset_dict["asset"] = (
            args.asset[1:]
            if len(args.asset) == 4 and args.asset[0] in ["Z", "X"]
            else args.asset
        )
        asset_dict["address"] = address["address"]
        asset_dict["new"] = address.get("new", False)
        asset_dict["expiretm"] = (
            int(address.get("expiretm", 0)) > 0
            and format_timestamp(int(address.get("expiretm", 0)))
            or ""
        )
        addresses_list.append(asset_dict)

    if not addresses_list:
        return

    # sort by expiretm
    addresses_list = sorted(addresses_list, key=lambda odict: odict["expiretm"])

    if args.csv:
        print(csv(addresses_list, headers="keys"))
    else:
        print(tabulate(addresses_list, headers="keys"))


def init(subparsers):
    parser_deposit_addresses = subparsers.add_parser(
        "deposit_addresses",
        aliases=["da"],
        help="[private] Get deposit addresses",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    for (args, kwargs) in OPTIONS:
        parser_deposit_addresses.add_argument(*args, **kwargs)
    parser_deposit_addresses.set_defaults(sub_func=get_deposit_addresses_cmd)
