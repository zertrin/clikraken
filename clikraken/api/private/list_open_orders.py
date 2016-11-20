# -*- coding: utf8 -*-

"""
clikraken.api.private.list_open_orders

This module queries the OpenOrders method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENCE file.
"""

from decimal import Decimal

from tabulate import tabulate

from clikraken.api.api_utils import parse_order_res, query_api
from clikraken.clikraken_utils import asset_pair_short, print_results


def list_open_orders(args):
    """List open orders."""

    # Parameters to pass to the API
    params = {
        # TODO
    }

    res = query_api('private', 'OpenOrders', params)
    if args.raw:
        print_results(res)

    res = res.get('result')
    if not res:
        return

    # extract list of orders from API results
    res_ol = res['open']

    # the parsing is done in an helper function
    ol = parse_order_res(res_ol, ['open'])

    # filter and sort orders by price in each category
    for otype in ol:
        # filter orders based on currency pair
        ol[otype] = [odict for odict in ol[otype]
                     if (odict['pair'] == asset_pair_short(args.pair) or args.pair == 'all')]
        # sort orders by price
        ol[otype] = sorted(ol[otype], key=lambda odict: Decimal(odict['price']))

    # final list is concatenation of buy orders followed by sell orders
    ol_all = ol['buy'] + ol['sell']

    if not ol_all:
        return

    print(tabulate(ol_all, headers="keys"))
