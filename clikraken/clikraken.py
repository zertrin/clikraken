#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
clikraken

Command line client for the Kraken exchange
"""

import argparse
import arrow
from collections import OrderedDict
from decimal import Decimal
import json
import krakenex
import os
import socket
import sys

from tabulate import tabulate

from . import __version__

KRAKEN_API_KEYFILE = os.path.expanduser('~/.config/kraken.key')

k = krakenex.API()
k.load_key(KRAKEN_API_KEYFILE)

TZ = 'Europe/Berlin'

# -----------------------------
# Helpers
# -----------------------------

date_field = {
    'open': 'opentm',
    'closed': 'closetm',
    'canceled': 'closetm',
    'expired': 'closetm'
}

date_label = {
    'open': 'opening_date',
    'closed': 'closing_date',
    'canceled': 'closing_date',
    'expired': 'closing_date'
}


def parse_order_res(in_ol, status_list_filter=None):
    ol = {'buy': [], 'sell': []}
    if status_list_filter is None:
        status_list_filter = ['open', 'closed']

    for txid in in_ol:
        o = in_ol[txid]
        ostatus = o['status']
        odict = OrderedDict()

        odict['orderid'] = txid
        odict['status'] = ostatus
        odict['type'] = o['descr']['type']
        odict['vol'] = o['vol']

        if ostatus != 'open':
            odict['vol_exec'] = o['vol_exec']

        odict['pair'] = o['descr']['pair']
        odict['ordertype'] = o['descr']['ordertype']

        if ostatus == 'open':
            odict['price'] = o['descr']['price']
        else:
            odict['price'] = o['price']

        if ostatus != 'open':
            odict['cost'] = o['cost']
            odict['fee'] = o['fee']

        odict['viqc'] = ('viqc' in o['oflags'])
        odict[date_label[ostatus]] = format_timestamp(o[date_field[ostatus]])

        if ostatus in status_list_filter:
            ol.get(odict['type']).append(odict)

    return ol


def humanize_timestamp(ts):
    return arrow.get(ts).humanize()


def format_timestamp(ts):
    return arrow.get(ts).to(TZ).replace(microsecond=0).format('YYYY-MM-DD HH:mm:ss')


def print_results(res):
    print(json.dumps(res, indent=2))


def asset_pair_short(ap_str):
    """Convert XETHZEUR to ETHEUR"""
    return ap_str[1:4] + ap_str[5:]


def query_api(api_type, *args):
    res = {}
    api_func = {
        'public': k.query_public,
        'private': k.query_private
    }
    func = api_func.get(api_type)
    if func is not None:
        try:
            res = api_func[api_type](*args)
        except (socket.timeout, socket.error) as e:
            print('Error while querying API!')
            print(repr(e))
    return res


# -----------------------------
# Public API
# -----------------------------


def ticker(args):
    params = {
        'pair': args.pair,
    }
    res = query_api('public', 'Ticker', params)
    if args.raw:
        print_results(res)

    res = res.get('result')
    if not res:
        return

    ticker_list = []
    for pair in res:
        pair_res = res[pair]
        pticker = OrderedDict()
        pticker['pair'] = asset_pair_short(pair)
        pticker['last'] = pair_res['c'][0]
        pticker['high'] = pair_res['h'][1]  # last 24h
        pticker['low'] = pair_res['l'][1]   # last 24h
        pticker['vol'] = pair_res['v'][1]   # last 24h
        pticker['wavg'] = pair_res['p'][1]  # last 24h
        quote_val = round(Decimal(pticker['vol']) * Decimal(pticker['wavg']) / 1000)
        pticker['vol value'] = str(quote_val) + ' k' + pticker['pair'][-3:]
        pticker['ask'] = pair_res['a'][0]
        pticker['bid'] = pair_res['b'][0]
        ticker_list.append(pticker)

    if not ticker_list:
        return

    ticker_list = sorted(ticker_list, key=lambda pticker: pticker['pair'])

    print(tabulate(ticker_list, headers="keys"))


def depth(args):
    params = {
        'pair': args.pair,
        'count': args.count
    }

    res = query_api('public', 'Depth', params)

    if args.raw:
        print_results(res)

    res = res.get('result')
    if not res:
        return

    depth_dict = {'asks': [], 'bids': []}
    depth_label = {'asks': "Ask", 'bids': "Bid"}

    shortpair = asset_pair_short(args.pair)

    for dtype in ['asks', 'bids']:
        dlist = res[args.pair][dtype]
        price_label = shortpair + " " + depth_label[dtype]

        for delem in dlist:
            dentry = OrderedDict()
            dentry[price_label] = delem[0]
            dentry["Volume"] = delem[1]
            dentry["Age"] = humanize_timestamp(delem[2])
            depth_dict[dtype].append(dentry)

        if not dlist:
            continue

        depth_dict[dtype] = reversed(sorted(depth_dict[dtype], key=lambda dentry: dentry[price_label]))

    asks_table = tabulate(depth_dict['asks'], headers="keys")
    bids_table = tabulate(depth_dict['bids'], headers="keys")

    print("{}\n\n{}".format(asks_table, bids_table))


def last_trades(args):
    params = {
        'pair': args.pair,
    }
    if args.since:
        params['since'] = args.since

    res = query_api('public', 'Trades', params)
    if args.raw:
        print_results(res)

    res = res.get('result')
    if not res:
        return

    results = res[args.pair]
    last_id = res['last']

    tlist = []
    ttype_label = {'b': 'buy', 's': 'sell'}
    otype_label = {'l': 'limit', 'm': 'market'}

    for trade in results:
        tdict = OrderedDict()
        tdict["Trade type"] = ttype_label.get(trade[3], 'unknown')
        tdict["Order type"] = otype_label.get(trade[4], 'unknown')
        tdict["Price"] = trade[0]
        tdict["Volume"] = trade[1]
        tdict["Age"] = humanize_timestamp(trade[2])
        # tdict["Misc"] = trade[5]
        tlist.append(tdict)

    if not tlist:
        return

    tlist = tlist[::-1]
    print(tabulate(tlist[:args.count], headers="keys") + '\n')

    sell_trades = [x for x in tlist if x["Trade type"] == "sell"]
    buy_trades  = [x for x in tlist if x["Trade type"] == "buy"]

    if sell_trades:
        last_sell = sell_trades[0]
        print('Last Sell = {} € -- {} -- {}'.format(last_sell["Price"], last_sell["Volume"], last_sell["Age"]))

    if buy_trades:
        last_buy = buy_trades[0]
        print('Last Buy =  {} € -- {} -- {}'.format(last_buy["Price"], last_buy["Volume"], last_buy["Age"]))

    print('Last ID = {}'.format(last_id))


# -----------------------------
# Private API
# -----------------------------


def get_balance(args=None):
    params = {}
    res = query_api('private', 'Balance', params)
    if args.raw:
        print_results(res)

    res = res.get('result')
    if not res:
        return

    bal_list = []
    for asset in res:
        asset_dict = OrderedDict()
        asset_dict['asset'] = asset[1:]
        asset_dict['balance'] = res[asset]
        bal_list.append(asset_dict)

    if not bal_list:
        return

    bal_list = sorted(bal_list, key=lambda asset_dict: asset_dict['asset'])

    print(tabulate(bal_list, headers="keys"))


def list_open_orders(args):
    params = {
        # TODO
    }
    res = query_api('private', 'OpenOrders', params)
    if args.raw:
        print_results(res)

    res = res.get('result')
    if not res:
        return

    res_ol = res['open']  # extract list of orders
    ol = parse_order_res(res_ol, ['open'])

    # filter and sort orders by price in each category
    for otype in ol:
        # filter orders
        ol[otype] = [odict for odict in ol[otype]
                     if (odict['pair'] == asset_pair_short(args.pair) or args.pair == 'all')]
        # sort orders by price
        ol[otype] = sorted(ol[otype], key=lambda odict: odict['price'])

    ol_all = ol['buy'] + ol['sell']
    if not ol_all:
        return

    print(tabulate(ol_all, headers="keys"))


def list_closed_orders(args):
    params = {
        # TODO
    }
    res = query_api('private', 'ClosedOrders', params)
    if args.raw:
        print_results(res)

    res = res.get('result')
    if not res:
        return

    res_ol = res['closed']  # extract list of orders
    ol = parse_order_res(res_ol, ['closed', 'canceled'])

    # mix order types
    ol = ol['buy'] + ol['sell']
    # filter out orders with zero volume executed
    ol = [odict for odict in ol
          if Decimal(odict['vol_exec']) > 0
          and (odict['pair'] == asset_pair_short(args.pair) or args.pair == 'all')]
    if not ol:
        return
    # sort by date
    ol = sorted(ol, key=lambda odict: odict['closing_date'])

    print(tabulate(ol, headers="keys"))


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

    res = query_api('private', 'AddOrder', params)
    if args.raw or True:  # TODO
        print_results(res)


def cancel_order(args):
    params = {
        'txid': args.order_id,
    }
    res = query_api('private', 'CancelOrder', params)
    if args.raw or True:  # TODO
        print_results(res)


def version(args=None):
    print('clikraken version: {}'.format(__version__))


def parse_args():
    parser = argparse.ArgumentParser(description='Command line client for the Kraken exchange')
    parser.add_argument('-v', '--version', action='store_const', const=version, dest='main_func',
                        help='Show program version')
    parser.add_argument('--raw', action='store_true', help='Output raw json results')
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
    parser_depth.add_argument('-c', '--count', type=int, default=7)
    parser_depth.set_defaults(sub_func=depth)

    parser_last_trades = subparsers.add_parser('last_trades', help='[public] Get the last trades')
    parser_last_trades.add_argument('-p', '--pair', default='XETHZEUR')
    parser_last_trades.add_argument('-s', '--since', default=None)
    parser_last_trades.add_argument('-c', '--count', type=int, default=15)
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
    parser_olist.add_argument('-p', '--pair', default='XETHZEUR')
    parser_olist.set_defaults(sub_func=list_open_orders)

    parser_clist = subparsers.add_parser('clist', help='[private] Get a list of your closed orders')
    parser_clist.add_argument('-p', '--pair', default='XETHZEUR')
    parser_clist.set_defaults(sub_func=list_closed_orders)

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
