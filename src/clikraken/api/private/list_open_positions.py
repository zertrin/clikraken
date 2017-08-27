# -*- coding: utf8 -*-

"""
clikraken.api.private.list_open_positions

This module queries the OpenPositions method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

from datetime import datetime

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import _tabulate as tabulate


def list_open_positions(args):
    """List open positions."""

    # Parameters to pass to the API
    api_params = {
        'docalcs': 'true',
    }

    res = query_api('private', 'OpenPositions', api_params, args)

    for order in res.values():
        # decode timestamp from unix time
        order['time'] = datetime.fromtimestamp(order['time'])

    # TODO pretty print
    print(tabulate(res.values(), headers="keys"))
