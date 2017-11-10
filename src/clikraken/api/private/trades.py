# -*- coding: utf8 -*-

"""
clikraken.api.private.trades

This module queries the TradesHistory or QueryTrades method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

from collections import OrderedDict

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import asset_pair_short
from clikraken.clikraken_utils import csv, format_timestamp
from clikraken.clikraken_utils import _tabulate as tabulate


def trades(args):
    """Get trades history or Query trades info"""

    # Parameters to pass to the API
    api_params = {
        # TODO: trades param
    }
    if args.type:
        api_params.update({'type': args.type})
    if args.start:
        api_params.update({'start': args.start})
    if args.end:
        api_params.update({'end': args.end})
    if args.ofs:
        api_params.update({'ofs': args.ofs})

    if args.id:
        api_params.update({
            'txid': args.id,
        })
        res_trades = query_api('private', 'QueryTrades', api_params, args)
    else:
        res = query_api('private', 'TradesHistory', api_params, args)
        # extract list of orders from API results
        res_trades = res['trades']

    # put all in a list
    tl = []
    for trade_id, trade_data in res_trades.items():
        trade_data.update({'tradeid': trade_id})
        tl += [trade_data]

    # filter orders based on currency pair
    if 'pair' in args and args.pair:
        tl = [td for td in tl if (td['pair'] in [args.pair, asset_pair_short(args.pair)] or args.pair == 'all')]

    # Lets get some order and filter some unnecessary fields
    tl2 = []
    for trade_data in tl:
        trade_dict = OrderedDict()
        trade_dict['txid'] = trade_data['tradeid']
        trade_dict['time'] = format_timestamp(int(trade_data['time']))
        trade_dict['pair'] = trade_data['pair'][1:] if len(trade_data['pair']) == 4 and \
            trade_data['pair'][0] in ['Z', 'X'] else trade_data['pair']
        trade_dict['type'] = trade_data['type']
        trade_dict['ordertype'] = trade_data['ordertype']
        trade_dict['vol'] = trade_data['vol']
        trade_dict['price'] = trade_data['price']
        trade_dict['cost'] = trade_data['cost']
        trade_dict['fee'] = trade_data['fee']
        trade_dict['margin'] = trade_data['margin']
        trade_dict['ordertxid'] = trade_data['ordertxid']
        trade_dict['misc'] = trade_data['misc']
        tl2.append(trade_dict)

    # sort orders by time
    tl2 = sorted(tl2, key=lambda x: x['time'])

    if not tl2:
        return

    if args.csv:
        print(csv(tl2, headers="keys"))
    else:
        print(tabulate(tl2, headers="keys"))
