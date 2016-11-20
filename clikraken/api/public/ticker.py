# -*- coding: utf8 -*-

"""
clikraken.api.public.ticker

This module queries the Ticker method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENCE file.
"""

from collections import OrderedDict
from decimal import Decimal

from tabulate import tabulate

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import asset_pair_short, print_results


def ticker(args):
    """Get currency ticker information."""

    # Parameters to pass to the API
    params = {
        'pair': args.pair,
    }

    res = query_api('public', 'Ticker', params)
    if args.raw:
        print_results(res)

    res = res.get('result')
    if not res:
        return

    # the list will contain one OrderedDict containing
    # the parser ticker info per asset pair
    ticker_list = []

    for pair in res:
        # extract the results for the current pair
        pair_res = res[pair]

        # Initialize an OrderedDict to garantee the column order
        # for later use with the tabulate function
        pticker = OrderedDict()

        pticker['pair'] = asset_pair_short(pair)
        pticker['last'] = pair_res['c'][0]  # price only
        pticker['high'] = pair_res['h'][1]  # last 24h
        pticker['low'] = pair_res['l'][1]   # last 24h
        pticker['vol'] = pair_res['v'][1]   # last 24h
        pticker['wavg'] = pair_res['p'][1]  # last 24h

        # calculate an estimate of the traded volume in quoted currency
        # for the last 24h: Volume x Average price
        quote_val = Decimal(pticker['vol']) * Decimal(pticker['wavg'])

        unit_prefix = ''
        if quote_val >= 10e6:
            quote_val = quote_val / Decimal(1e6)
            unit_prefix = 'M'
        elif quote_val >= 10e3:
            quote_val = quote_val / Decimal(1e3)
            unit_prefix = 'k'

        pticker['vol value'] = str(round(quote_val)) + ' ' + unit_prefix + pticker['pair'][-3:]

        # get the price only
        pticker['ask'] = pair_res['a'][0]
        pticker['bid'] = pair_res['b'][0]

        ticker_list.append(pticker)

    if not ticker_list:
        return

    ticker_list = sorted(ticker_list, key=lambda pticker: pticker['pair'])

    print(tabulate(ticker_list, headers="keys"))
