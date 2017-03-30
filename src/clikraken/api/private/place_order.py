# -*- coding: utf8 -*-

"""
clikraken.api.private.place_order

This module queries the AddOrder method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import clikraken.global_vars as gv

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import check_trading_agreement
from clikraken.log_utils import logger


def place_order(args):
    """Place an order."""

    # Parameters to pass to the API
    api_params = {
        'pair': args.pair,
        'type': args.type,
        'ordertype': args.ordertype,
        'volume': args.volume,
        'starttm': args.starttm,
        'expiretm': args.expiretm,
    }

    if gv.TRADING_AGREEMENT == 'agree':
        api_params['trading_agreement'] = 'agree'

    if args.ordertype == 'limit':
        if args.price is None:
            logger.error('For limit orders, the price must be given!')
            return
        else:
            api_params['price'] = args.price
    elif args.ordertype == 'market':
        if args.price is not None:
            logger.warn('price is ignored for market orders!')
        check_trading_agreement()

    oflags = []  # order flags
    if args.ordertype == 'limit':
        # for limit orders, always set post only order flag
        oflags.append('post')
    if args.viqc:
        oflags.append('viqc')
    if oflags:
        api_params['oflags'] = ','.join(oflags)

    if args.validate:
        api_params['validate'] = 'true'

    res = query_api('private', 'AddOrder', api_params, args)

    descr = res.get('descr')
    odesc = descr.get('order', 'No description available!')
    print(odesc)

    txid = res.get('txid')

    if not txid:
        if args.validate:
            logger.info('Validating inputs only. Order not submitted!')
        else:
            logger.warn('Order was NOT successfully added!')
    else:
        for tx in txid:
            print(tx)
