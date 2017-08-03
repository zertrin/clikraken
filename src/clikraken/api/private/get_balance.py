# -*- coding: utf8 -*-

"""
clikraken.api.private.get_balance

This module queries the Balance method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

from collections import OrderedDict

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import _tabulate as tabulate


def get_balance(args=None):
    """Get user balance."""

    # Parameters to pass to the API
    api_params = {}

    res = query_api('private', 'Balance', api_params, args)

    bal_list = []
    for asset in res:
        # Initialize an OrderedDict to garantee the column order
        # for later use with the tabulate function
        asset_dict = OrderedDict()
        # Remove leading Z or X from asset pair if it is of length 4
        asset_dict['asset'] = asset[1:] if len(asset) == 4 and asset[0] in ['Z', 'X'] else asset
        asset_dict['balance'] = res[asset]
        bal_list.append(asset_dict)

    if not bal_list:
        return

    # Sort alphabetically
    bal_list = sorted(bal_list, key=lambda asset_dict: asset_dict['asset'])

    print(tabulate(bal_list, headers="keys"))
