# -*- coding: utf8 -*-

"""
clikraken.api.private.list_open_positions

This module queries the OpenPositions method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

from datetime import datetime
from collections import OrderedDict

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import _tabulate as tabulate


def list_open_positions(args):
    """List open positions."""

    # Parameters to pass to the API
    api_params = {
        'docalcs': 'true',
    }

    res = query_api('private', 'OpenPositions', api_params, args)

    pos_list = []
    for order in res.values():
        pos = OrderedDict()
        pos['ordertxid'] = order['ordertxid']
        pos['opening time'] = datetime.fromtimestamp(order['time'])
        pos['type'] = order['type']
        pos['volume'] = order['vol']
        pos['pair'] = order['pair']
        pos['ordertype'] = order['ordertype']
        pos['cost'] = order['cost']
        pos['fee'] = order['fee']
        pos['margin'] = order['margin']
        pos['value'] = order['value']
        pos['profit/loss'] = order['net']
        pos['rollover time'] = datetime.fromtimestamp(int(order['rollovertm']))
        pos['rollover terms'] = order['terms']

        pos_list.append(pos)

    print(tabulate(pos_list, headers="keys"))
