# -*- coding: utf8 -*-

"""
clikraken.api.private.cancel_order

This module queries the CancelOrder method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

from clikraken.api.api_utils import query_api
from clikraken.log_utils import logger


def cancel_order(args):
    """Cancel an open order."""

    for order_id in args.order_ids:
        # Parameters to pass to the API
        api_params = {
            'txid': order_id,
        }

        res = query_api('private', 'CancelOrder', api_params, args)

        count = res.get('count')
        pending = res.get('pending')

        if count:
            print('{} - count: {}'.format(order_id, count))
        if pending:
            logger.info('{} - order(s) is/are pending cancellation!'.format(order_id))
