# -*- coding: utf8 -*-

"""
clikraken.api.public.asset_pairs

This module queries the AssetPairs method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

from collections import OrderedDict

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import _tabulate as tabulate
from clikraken.clikraken_utils import csv, file


def asset_pairs(args):
    """Get available asset pairs."""

    # Parameters to pass to the API
    api_params = {}

    res = query_api('public', 'AssetPairs', api_params, args)

    # initialize a list to store the parsed assets pairs
    assetlist = []

    for assetpair in res:
        if assetpair.endswith('.d'):
            continue
        ad = OrderedDict()
        ad['Pair'] = assetpair
        ad['Alt Name'] = res[assetpair]['altname']
        ad['Base'] = res[assetpair]['base']
        ad['Quote'] = res[assetpair]['quote']
        assetlist.append(ad)

    if args.csv:
        output = csv(assetlist, headers="keys")
    else:
        output = (tabulate(assetlist, headers='keys')
                  + '\n--- Total: {} pairs'.format(len(assetlist))
                  )

    print(output)

    if args.fileout:
        file(output)
