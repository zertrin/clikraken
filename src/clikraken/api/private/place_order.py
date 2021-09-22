# -*- coding: utf-8 -*-

"""
clikraken.api.private.place_order

This module queries the AddOrder method of Kraken's API
and outputs the results in a tabular format.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import argparse
from collections import namedtuple
from decimal import Decimal

import clikraken.global_vars as gv

from clikraken.api.api_utils import query_api
from clikraken.clikraken_utils import check_trading_agreement
from clikraken.log_utils import logger


def place_order(
    type,
    pair,
    ordertype,
    volume,
    price=None,
    price2=None,
    validate=False,
    starttm=0,
    expiretm=0,
    leverage="none",
    viqc=False,
    userref=False,
):
    Args = namedtuple(
        "Args",
        [
            "debug",
            "raw",
            "json",
            "csv",
            "pair",
            "type",
            "ordertype",
            "volume",
            "price",
            "price2",
            "validate",
            "starttm",
            "expiretm",
            "leverage",
            "viqc",
            "userref",
        ],
    )
    args = Args(
        False,
        False,
        False,
        False,
        type=type,
        pair=pair,
        ordertype=ordertype,
        volume=volume,
        price=price,
        price2=price2,
        validate=validate,
        starttm=starttm,
        expiretm=expiretm,
        leverage=leverage,
        viqc=viqc,
        userref=userref,
    )

    return place_order_api(args)


def place_order_api(args):
    """Place an order."""

    # Parameters to pass to the API
    api_params = {
        "pair": args.pair,
        "type": args.type,
        "ordertype": args.ordertype,
        "volume": args.volume,
        "starttm": args.starttm,
        "expiretm": args.expiretm,
        "leverage": args.leverage,
    }

    if gv.TRADING_AGREEMENT == "agree":
        api_params["trading_agreement"] = "agree"

    if args.ordertype == "limit":
        if args.price is None:
            logger.error("For limit orders, the price must be given!")
            return
        else:
            api_params["price"] = args.price
    elif args.ordertype == "market":
        if args.price is not None:
            logger.warn("price is ignored for market orders!")
        check_trading_agreement()

    if args.userref:
        api_params["userref"] = args.userref

    oflags = []  # order flags
    if args.ordertype == "limit":
        if not args.nopost:
            # for limit orders, by default set post-only order flag
            oflags.append("post")
    if args.viqc:
        oflags.append("viqc")
    if oflags:
        api_params["oflags"] = ",".join(oflags)

    if args.validate:
        api_params["validate"] = "true"

    res = query_api("private", "AddOrder", api_params, args)
    return res


def place_order_cmd(args):
    """Place an order."""

    res = place_order_api(args)

    descr = res.get("descr")
    odesc = descr.get("order", "No description available!")
    print(odesc)

    txid = res.get("txid")

    if not txid:
        if args.validate:
            logger.info("Validating inputs only. Order not submitted!")
        else:
            logger.warn("Order was NOT successfully added!")
    else:
        for tx in txid:
            print(tx)


def init(subparsers):
    pair_help = "asset pair"
    parser_place = subparsers.add_parser(
        "place",
        aliases=["p"],
        help="[private] Place an order",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_place.add_argument("type", choices=["sell", "buy"])
    parser_place.add_argument("volume", type=Decimal)
    parser_place.add_argument("price", default=None, nargs="?")
    parser_place.add_argument(
        "-l", "--leverage", default="none", help="leverage for margin trading"
    )
    parser_place.add_argument("-p", "--pair", default=gv.DEFAULT_PAIR, help=pair_help)
    parser_place.add_argument(
        "-t",
        "--ordertype",
        choices=["market", "limit"],
        default="limit",
        help="order type. Currently implemented: [limit, market].",
    )
    parser_place.add_argument("-s", "--starttm", default=0, help="scheduled start time")
    parser_place.add_argument("-e", "--expiretm", default=0, help="expiration time")
    parser_place.add_argument(
        "-r", "--userref", help="user reference id.  32-bit signed number.  (optional)"
    )
    parser_place.add_argument(
        "-q", "--viqc", action="store_true", help="volume in quote currency"
    )
    parser_place.add_argument(
        "-T",
        "--nopost",
        action="store_true",
        help="disable 'post-only' option (for limit taker orders)",
    )
    parser_place.add_argument(
        "-v",
        "--validate",
        action="store_true",
        help="validate inputs only. do not submit order",
    )
    parser_place.set_defaults(sub_func=place_order_cmd)
