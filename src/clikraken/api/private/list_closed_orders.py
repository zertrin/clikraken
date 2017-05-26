# -*- coding: utf8 -*-

"""
clikraken.api.private.list_list_closed_orders

This module queries the ClosedOrders method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

from decimal import Decimal

from clikraken.api.api_utils import parse_order_res, query_api
from clikraken.clikraken_utils import asset_pair_short
from clikraken.clikraken_utils import _tabulate as tabulate


def list_closed_orders(args):
    """List closed orders."""

    # Parameters to pass to the API
    api_params = {
        # TODO
    }

    res = query_api('private', 'ClosedOrders', api_params, args)

    # extract list of orders from API results
    res_ol = res['closed']

    # the parsing is done in an helper function
    ol = parse_order_res(res_ol, ['closed', 'canceled'])

    # merge order types in one list
    ol = ol['buy'] + ol['sell']

    # filter out orders with zero volume executed
    ol = [odict for odict in ol if Decimal(odict['vol_exec']) > 0]
    if 'pair' in args and args.pair:
        ol = [odict for odict in ol if odict['pair'] in [args.pair, asset_pair_short(args.pair)]]

    if not ol:
        return

    # sort by date
    ol = sorted(ol, key=lambda odict: odict['closing_date'])

    print(tabulate(ol, headers="keys"))
