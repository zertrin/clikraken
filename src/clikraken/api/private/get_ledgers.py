# -*- coding: utf8 -*-

"""
clikraken.api.private.get_ledgers

This module queries the Ledgers or QueryLedgers method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

from collections import OrderedDict

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import _tabulate as tabulate
from clikraken.clikraken_utils import csv
from clikraken.clikraken_utils import format_timestamp


def get_ledgers(args):
    """Get ledgers info"""

    # If id is specified, then query just that
    if args.id:
        api_params = {
            'id': args.id,
        }
        lg = query_api('private', 'QueryLedgers', api_params, args)
    else:
        # Parameters to pass to the API
        api_params = {
        }
        if args.asset:  # We do not user DEFAULT_ASSET HERE as this param is optional
            api_params.update({'asset': args.asset})
        if args.type:
            api_params.update({'type': args.type})
        if args.start:
            api_params.update({'start': args.start})
        if args.end:
            api_params.update({'end': args.end})
        if args.ofs:
            api_params.update({'ofs': args.ofs})
        res = query_api('private', 'Ledgers', api_params, args)
        # extract list of ledgers from API results
        lg = res['ledger']

    lg_list = []
    for refid, item in lg.items():
        # Initialize an OrderedDict to garantee the column order
        # for later use with the tabulate function
        asset_dict = OrderedDict()
        asset_dict['id'] = refid
        asset_dict['refid'] = item['refid']
        asset_dict['time'] = format_timestamp(int(item['time']))
        asset_dict['type'] = item['type']
        # Remove leading Z or X from item pair if it is of length 4
        asset_dict['asset'] = item['asset'][1:] \
            if len(item['asset']) == 4 and item['asset'][0] in ['Z', 'X'] else item['asset']
        asset_dict['aclass'] = item['aclass']
        asset_dict['amount'] = float(item['amount'])
        asset_dict['fee'] = float(item['fee'])
        asset_dict['balance'] = float(item['balance'])

        lg_list.append(asset_dict)

    if not lg_list:
        return

    # sort by date
    lg_list = sorted(lg_list, key=lambda odict: odict['time'])

    if args.csv:
        print(csv(lg_list, headers="keys"))
    else:
        print(tabulate(lg_list, headers="keys"))
