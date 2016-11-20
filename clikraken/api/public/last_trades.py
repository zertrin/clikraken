# -*- coding: utf8 -*-

"""
clikraken.api.public.last_trades

This module queries the Trades method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENCE file.
"""

from collections import OrderedDict

from tabulate import tabulate

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import print_results, humanize_timestamp, quote_currency_from_asset_pair


def last_trades(args):
    """Get last trades."""

    quote_currency = quote_currency_from_asset_pair(args.pair)

    # Parameters to pass to the API
    params = {
        'pair': args.pair,
    }
    if args.since:
        params['since'] = args.since

    res = query_api('public', 'Trades', params)
    if args.raw:
        print_results(res)

    res = res.get('result')
    if not res:
        return

    results = res[args.pair]
    last_id = res['last']

    # initialize a list to store the parsed trades
    tlist = []

    # mappings
    ttype_label = {'b': 'buy', 's': 'sell'}
    otype_label = {'l': 'limit', 'm': 'market'}

    for trade in results:
        # Initialize an OrderedDict to garantee the column order
        # for later use with the tabulate function
        tdict = OrderedDict()
        tdict["Trade type"] = ttype_label.get(trade[3], 'unknown')
        tdict["Order type"] = otype_label.get(trade[4], 'unknown')
        tdict["Price"] = trade[0]
        tdict["Volume"] = trade[1]
        tdict["Age"] = humanize_timestamp(trade[2])
        # tdict["Misc"] = trade[5]
        tlist.append(tdict)

    if not tlist:
        return

    # Reverse trade list to have the most recent trades at the top
    tlist = tlist[::-1]

    print(tabulate(tlist[:args.count], headers="keys") + '\n')

    # separate the trades based on their type
    sell_trades = [x for x in tlist if x["Trade type"] == "sell"]
    buy_trades = [x for x in tlist if x["Trade type"] == "buy"]

    last_sell = sell_trades[0]
    last_buy = buy_trades[0]
    lt = [
        ["", "Price ("+quote_currency+")", "Volume", "Age"],
        ["Last Sell", last_sell["Price"], last_sell["Volume"], last_sell["Age"]],
        ["Last Buy", last_buy["Price"], last_buy["Volume"], last_buy["Age"]],
    ]

    print(tabulate(lt, headers="firstrow") + '\n')

    print('Last ID = {}'.format(last_id))
