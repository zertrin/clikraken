# -*- coding: utf-8 -*-

"""
clikraken.api.private.cancel_order

This module queries the CancelOrder method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import argparse

from clikraken.api.api_utils import query_api
from clikraken.log_utils import logger
from clikraken.clikraken_utils import process_options

OPTIONS = ((("order_ids",), {"type": str, "nargs": "+", "help": "transaction ids"}),)

MANDATORY_OPTIONS = ("order_ids",)


def cancel_order(**kwargs):
    """Cancel an open order."""
    args = process_options(kwargs, OPTIONS, MANDATORY_OPTIONS)

    return cancel_order_api(args)


def cancel_order_api(args):
    """Cancel an open order."""

    res = {}
    for order_id in args.order_ids:
        # Parameters to pass to the API
        api_params = {
            "txid": order_id,
        }

        res[order_id] = query_api("private", "CancelOrder", api_params, args)
    return res


def cancel_order_cmd(args):
    """Cancel an open order."""
    dct = cancel_order_api(args)

    for order_id in dct:
        res = dct[order_id]
        count = res.get("count")
        pending = res.get("pending")

        if count:
            print("{} - count: {}".format(order_id, count))
        if pending:
            logger.info("{} - order(s) is/are pending cancellation!".format(order_id))


def init(subparsers):
    parser_cancel = subparsers.add_parser(
        "cancel",
        aliases=["x"],
        help="[private] Cancel orders",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    for (args, kwargs) in OPTIONS:
        parser_cancel.add_argument(*args, **kwargs)
    parser_cancel.set_defaults(sub_func=cancel_order_cmd)
