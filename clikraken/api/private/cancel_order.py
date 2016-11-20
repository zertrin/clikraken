# -*- coding: utf8 -*-

"""
clikraken.api.private.cancel_order

This module queries the CancelOrder method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENCE file.
"""

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import print_results
from clikraken.log_utils import logger


def cancel_order(args):
    """Cancel an open order."""

    # Parameters to pass to the API
    params = {
        'txid': args.order_id,
    }

    res = query_api('private', 'CancelOrder', params)
    if args.raw:
        print_results(res)

    res = res.get('result')
    if not res:
        return

    count = res.get('count')
    pending = res.get('pending')

    if count:
        print('count: {}'.format(count))
    if pending:
        logger.info('order(s) is/are pending cancellation!')
