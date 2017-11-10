# -*- coding: utf8 -*-

"""
clikraken.api.private.withdraw

This module queries the DepositAddresses method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

from collections import OrderedDict

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import format_timestamp
from clikraken.clikraken_utils import _tabulate as tabulate


def withdraw(args=None):
    """Withdraw funds"""

    # Parameters to pass to the API
    api_params = {
        'asset': args.asset,
        'key': args.key,
        'amount': args.amount,
    }

    res = query_api('private', 'Withdraw', api_params, args)

    if not res:
        return

    print(res)
    # TODO: show example command to get query this withdrawal status
