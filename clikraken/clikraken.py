#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
clikraken

Command line client for the Kraken exchange
"""

import argparse
import arrow
from decimal import Decimal
import json
import krakenex
import os
import sys

from . import __version__

KRAKEN_API_KEYFILE = os.path.expanduser('~/.config/kraken.key')

k = krakenex.API()
k.load_key(KRAKEN_API_KEYFILE)


def print_results(res):
    print(json.dumps(res, indent=2))


def ticker(args):
    params = {
        'pair': args.pair,
    }
    res = k.query_public('Ticker', params)
    print_results(res)


def depth(args):
    params = {
        'pair': args.pair,
        'count': args.count
    }
    res = k.query_public('Depth', params)
    print_results(res)


def last_trades(args):
    params = {
        'pair': args.pair,
    }
    if args.since:
        params['since'] = args.since

    res = k.query_public('Trades', params)
    print_results(res)

    results = res['result'][args.pair]
    last_id = res['result']['last']
    sell_trades = [x for x in results if x[3] == "s"]
    buy_trades  = [x for x in results if x[3] == "b"]

    if sell_trades:
        last_sell = [x for x in results if x[3] == "s"][-1]
        last_sell_price = last_sell[0]
        last_sell_volume = last_sell[1]
        last_sell_time = arrow.get(last_sell[2]).to('Europe/Berlin')
        print('Last Sell = {} € -- {} -- {}'.format(last_sell_price, last_sell_volume, last_sell_time))

    if buy_trades:
        last_buy  = [x for x in results if x[3] == "b"][-1]
        last_buy_price = last_buy[0]
        last_buy_volume = last_buy[1]
        last_buy_time = arrow.get(last_buy[2]).to('Europe/Berlin')
        print('Last Buy  = {} € -- {} -- {}'.format(last_buy_price, last_buy_volume, last_buy_time))

    print('Last ID = {}'.format(last_id))


def get_balance(args=None):
    params = {}
    res = k.query_private('Balance', params)
    print_results(res)


def list_orders(args):
    params = {
    }
    res = k.query_private('OpenOrders', params)
    print_results(res)


def place_order(args):
    oflags = []  # order flags
    if args.ordertype == 'limit':
        oflags.append('post')
    if args.viqc:
        oflags.append('viqc')

    params = {
        'pair': args.pair,
        'type': args.type,
        'ordertype': args.ordertype,
        'price': args.price,
        'volume': args.volume,
        'oflags': ','.join(oflags),
        'starttm': args.starttm,
        'expiretm': args.expiretm,
    }

    if args.validate:
        params['validate'] = 'true'

    res = k.query_private('AddOrder', params)
    print_results(res)


def cancel_order(args):
    params = {
        'txid': args.order_id,
    }
    res = k.query_private('CancelOrder', params)
    print_results(res)


def version(args=None):
    print('clikraken version: {}'.format(__version__))


def parse_args():
    parser = argparse.ArgumentParser(description='Command line client for the Kraken exchange')
    parser.add_argument('-v', '--version', action='store_const', const=version, dest='main_func')
    parser.set_defaults(main_func=None)

    subparsers = parser.add_subparsers(dest='subparser_name', help='available subcommands')

    # ----------
    # Public API
    # ----------

    parser_ticker = subparsers.add_parser('ticker', help='[public] Get the Ticker')
    parser_ticker.add_argument('-p', '--pair', default='XETHZEUR')
    parser_ticker.set_defaults(sub_func=ticker)

    parser_depth = subparsers.add_parser('depth', help='[public] Get the current market depth data')
    parser_depth.add_argument('-p', '--pair', default='XETHZEUR')
    parser_depth.add_argument('-c', '--count', type=int, default=5)
    parser_depth.set_defaults(sub_func=depth)

    parser_last_trades = subparsers.add_parser('last_trades', help='[public] Get the last trades')
    parser_last_trades.add_argument('-p', '--pair', default='XETHZEUR')
    parser_last_trades.add_argument('-since', '--since', default=None)
    parser_last_trades.set_defaults(sub_func=last_trades)

    # -----------
    # Private API
    # -----------

    parser_balance = subparsers.add_parser('balance', help='[private] Get your current balance')
    parser_balance.set_defaults(sub_func=get_balance)

    parser_place = subparsers.add_parser('place', help='[private] Place an order')
    parser_place.add_argument('type', choices=['sell', 'buy'])
    parser_place.add_argument('volume', type=Decimal)
    parser_place.add_argument('price', type=Decimal)
    parser_place.add_argument('-p', '--pair', default='XETHZEUR')
    parser_place.add_argument('-t', '--ordertype', choices=['market', 'limit'], default='limit')
    parser_place.add_argument('-s', '--starttm', default=0)
    parser_place.add_argument('-e', '--expiretm', default=0)
    parser_place.add_argument('-q', '--viqc', action='store_true')
    parser_place.add_argument('-v', '--validate', action='store_true')
    parser_place.set_defaults(sub_func=place_order)

    parser_cancel = subparsers.add_parser('cancel', help='[private] Cancel an order')
    parser_cancel.add_argument('order_id', type=str)
    parser_cancel.set_defaults(sub_func=cancel_order)

    parser_olist = subparsers.add_parser('olist', help='[private] Get a list of your open orders')
    parser_olist.set_defaults(sub_func=list_orders)

    args = parser.parse_args()

    # hack to work around Python bug #9351 https://bugs.python.org/issue9351
    if all([vars(args).get(f, None) is None
            for f in ['sub_func', 'main_func']]):
        parser.print_usage()
        sys.exit(0)

    return args


def main():
    args = parse_args()
    func = args.sub_func if 'sub_func' in args else args.main_func
    if func is not None:
        func(args)

if __name__ == "__main__":
    main()
