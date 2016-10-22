#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
clikraken

Command line client for the Kraken exchange
"""

import argparse
import arrow
from collections import OrderedDict
import configparser
from decimal import Decimal
import json
import krakenex
import os
import socket
import sys

from tabulate import tabulate

from . import __version__

# -----------------------------
# Kraken API keyfile
# -----------------------------

# Resolve userpath to an absolute path
KRAKEN_API_KEYFILE = os.path.expanduser('~/.config/clikraken/kraken.key')
USER_SETTINGS_PATH = os.path.expanduser('~/.config/clikraken/settings.ini')

# Instanciate the krakenex module to communicate with Kraken's API
k = krakenex.API()

# Load the API key of the user
k.load_key(KRAKEN_API_KEYFILE)

# -----------------------------
# Settings
# -----------------------------

# Default settings
DEFAULT_SETTINGS_INI = """[clikraken]
# default currency pair when no option '-p' or '--pair' is given
currency_pair = XETHZEUR
# Timezone for displaying date and time infos
timezone = Europe/Berlin
"""

config = configparser.ConfigParser()
config.read_string(DEFAULT_SETTINGS_INI)
config.read(USER_SETTINGS_PATH)

conf = config['clikraken']

DEFAULT_PAIR = conf.get('currency_pair')
TZ = conf.get('timezone')


def output_default_settings_ini(args):
    """Output the contents of the default settings.ini file"""
    print(DEFAULT_SETTINGS_INI)

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
    """
    Helper to parse the order results from the API.

    Depending on the status of the orders, different
    properties are available.

    See Kraken's API documentation for details.
    """

    # we will store the buy and sell orders separately during parsing
    ol = {'buy': [], 'sell': []}

    # status_list_filter is an optional argument of type list
    # the default value can't be set in the function signature
    if status_list_filter is None:
        status_list_filter = ['open', 'closed']

    # iterate over the given order list
    for txid in in_ol:
        # extract the current order dict
        o = in_ol[txid]

        ostatus = o['status']

        # We store the parsed orders in an OrderedDict to garantee
        # the order of columns for use later in the tabulate function.
        # (one key == "one column")
        odict = OrderedDict()

        odict['orderid'] = txid
        odict['status'] = ostatus
        odict['type'] = o['descr']['type']
        odict['vol'] = o['vol']

        # Volume executed is only available if the order isn't open
        # TODO: check if that's really true
        if ostatus != 'open':
            odict['vol_exec'] = o['vol_exec']

        odict['pair'] = o['descr']['pair']
        odict['ordertype'] = o['descr']['ordertype']

        # If the order is open, take the price from the order description
        # if the order is closed, take the average price
        if ostatus == 'open':
            odict['price'] = o['descr']['price']
        else:
            odict['price'] = o['price']

        # Cost and Fee are only available if the order isn't open
        if ostatus != 'open':
            odict['cost'] = o['cost']
            odict['fee'] = o['fee']

        odict['viqc'] = ('viqc' in o['oflags'])  # boolean check

        # date_label[ostatus] is the column name and changes
        # depending on the status of the order.
        odict[date_label[ostatus]] = format_timestamp(o[date_field[ostatus]])

        # filter here based on the list of status that we want
        if ostatus in status_list_filter:
            ol.get(odict['type']).append(odict)

    return ol


def humanize_timestamp(ts):
    """Humanize a UNIX timestamp."""
    return arrow.get(ts).humanize()


def format_timestamp(ts):
    """Format a UNIX timestamp to truncated ISO8601 format."""
    return arrow.get(ts).to(TZ).replace(microsecond=0).format('YYYY-MM-DD HH:mm:ss')


def print_results(res):
    """Pretty-print the JSON result from the API."""
    print(json.dumps(res, indent=2))


def asset_pair_short(ap_str):
    """Convert XETHZEUR to ETHEUR"""
    return ap_str[1:4] + ap_str[5:]


def query_api(api_type, *args):
    """
    Wrapper to query Kraken's API through krakenex
    and handle connection errors.
    """

    # default to empty dict because that's the expected return type
    res = {}

    # just a mapping from api_type to the function to be called
    api_func = {
        'public': k.query_public,
        'private': k.query_private
    }
    func = api_func.get(api_type)

    if func is not None:
        try:
            # call to the krakenex API
            res = api_func[api_type](*args)
        except (socket.timeout, socket.error, ValueError) as e:
            print('Error while querying API!')
            print(repr(e))

    err = res.get('error')
    for e in err:
        print('ERROR: {}'.format(e))

    return res


# -----------------------------
# Public API
# -----------------------------


def ticker(args):
    """Get currency ticker information."""

    # Parameters to pass to the API
    params = {
        'pair': args.pair,
    }

    res = query_api('public', 'Ticker', params)
    if args.raw:
        print_results(res)

    res = res.get('result')
    if not res:
        return

    # the list will contain one OrderedDict containing
    # the parser ticker info per asset pair
    ticker_list = []

    for pair in res:
        # extract the results for the current pair
        pair_res = res[pair]

        # Initialize an OrderedDict to garantee the column order
        # for later use with the tabulate function
        pticker = OrderedDict()

        pticker['pair'] = asset_pair_short(pair)
        pticker['last'] = pair_res['c'][0]  # price only
        pticker['high'] = pair_res['h'][1]  # last 24h
        pticker['low'] = pair_res['l'][1]   # last 24h
        pticker['vol'] = pair_res['v'][1]   # last 24h
        pticker['wavg'] = pair_res['p'][1]  # last 24h

        # calculate an estimate of the traded volume in quoted currency
        # for the last 24h: Volume x Average price
        quote_val = Decimal(pticker['vol']) * Decimal(pticker['wavg'])

        unit_prefix = ''
        if quote_val >= 10e6:
            quote_val = quote_val / Decimal(1e6)
            unit_prefix = 'M'
        elif quote_val >= 10e3:
            quote_val = quote_val / Decimal(1e3)
            unit_prefix = 'k'

        pticker['vol value'] = str(round(quote_val)) + ' ' + unit_prefix + pticker['pair'][-3:]

        # get the price only
        pticker['ask'] = pair_res['a'][0]
        pticker['bid'] = pair_res['b'][0]

        ticker_list.append(pticker)

    if not ticker_list:
        return

    ticker_list = sorted(ticker_list, key=lambda pticker: pticker['pair'])

    print(tabulate(ticker_list, headers="keys"))


def depth(args):
    """Get market depth information."""

    # Parameters to pass to the API
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

    # dtype is 'asks' or 'bids'
    for dtype in depth_dict:
        # extract the array of market depth from the api results
        dlist = res[args.pair][dtype]
        # build a column label depending on the asset pair and dtype
        price_label = shortpair + " " + depth_label[dtype]

        for delem in dlist:
            # Initialize an OrderedDict to garantee the column order
            # for later use with the tabulate function
            dentry = OrderedDict()
            dentry[price_label] = delem[0]
            dentry["Volume"] = delem[1]
            dentry["Age"] = humanize_timestamp(delem[2])
            depth_dict[dtype].append(dentry)

        if not dlist:
            continue

        # sort by price descending
        depth_dict[dtype] = reversed(sorted(depth_dict[dtype], key=lambda dentry: Decimal(dentry[price_label])))

    asks_table = tabulate(depth_dict['asks'], headers="keys")
    bids_table = tabulate(depth_dict['bids'], headers="keys")

    print("{}\n\n{}".format(asks_table, bids_table))


def last_trades(args):
    """Get last trades."""

    # Parameters to pass to the API
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

    # initialize a list to store the parsed trades
    tlist = []

    # mappings
    ttype_label = {'b': 'buy', 's': 'sell'}
    otype_label = {'l': 'limit', 'm': 'market'}

    for trade in results:
        # Initialize an OrderedDict to garantee the column order
        # for later use with the tabulate function
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

    # Reverse trade list to have the most recent trades at the top
    tlist = tlist[::-1]

    print(tabulate(tlist[:args.count], headers="keys") + '\n')

    # separate the trades based on their type
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
    """Get user balance."""

    # Parameters to pass to the API
    params = {}

    res = query_api('private', 'Balance', params)
    if args.raw:
        print_results(res)

    res = res.get('result')
    if not res:
        return

    bal_list = []
    for asset in res:
        # Initialize an OrderedDict to garantee the column order
        # for later use with the tabulate function
        asset_dict = OrderedDict()
        asset_dict['asset'] = asset[1:]  # skip first char (e.g. XXBT -> XBT)
        asset_dict['balance'] = res[asset]
        bal_list.append(asset_dict)

    if not bal_list:
        return

    # Sort alphabetically
    bal_list = sorted(bal_list, key=lambda asset_dict: asset_dict['asset'])

    print(tabulate(bal_list, headers="keys"))


def list_open_orders(args):
    """List open orders."""

    # Parameters to pass to the API
    params = {
        # TODO
    }

    res = query_api('private', 'OpenOrders', params)
    if args.raw:
        print_results(res)

    res = res.get('result')
    if not res:
        return

    # extract list of orders from API results
    res_ol = res['open']

    # the parsing is done in an helper function
    ol = parse_order_res(res_ol, ['open'])

    # filter and sort orders by price in each category
    for otype in ol:
        # filter orders based on currency pair
        ol[otype] = [odict for odict in ol[otype]
                     if (odict['pair'] == asset_pair_short(args.pair) or args.pair == 'all')]
        # sort orders by price
        ol[otype] = sorted(ol[otype], key=lambda odict: Decimal(odict['price']))

    # final list is concatenation of buy orders followed by sell orders
    ol_all = ol['buy'] + ol['sell']

    if not ol_all:
        return

    print(tabulate(ol_all, headers="keys"))


def list_closed_orders(args):
    """List closed orders."""

    # Parameters to pass to the API
    params = {
        # TODO
    }

    res = query_api('private', 'ClosedOrders', params)
    if args.raw:
        print_results(res)

    res = res.get('result')
    if not res:
        return

    # extract list of orders from API results
    res_ol = res['closed']

    # the parsing is done in an helper function
    ol = parse_order_res(res_ol, ['closed', 'canceled'])

    # merge order types in one list
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
    """Place an order."""

    oflags = []  # order flags
    if args.ordertype == 'limit':
        # for limit orders, always set post only order flag
        oflags.append('post')
    if args.viqc:
        oflags.append('viqc')

    # Parameters to pass to the API
    params = {
        'pair': args.pair,
        'type': args.type,
        'ordertype': args.ordertype,
        'volume': args.volume,
        'oflags': ','.join(oflags),
        'starttm': args.starttm,
        'expiretm': args.expiretm,
    }

    if args.ordertype == 'limit':
        if args.price is None:
            print('ERROR: For limit orders, the price must be given!')
            return
        else:
            params['price'] = args.price
    elif args.ordertype == 'market':
        if args.price is not None:
            print('WARNING: price is ignored for market orders!')

    if not oflags:
        # if oflags is empty, just remove it from the params
        params.pop('oflags', None)

    if args.validate:
        params['validate'] = 'true'

    res = query_api('private', 'AddOrder', params)
    if args.raw:
        print_results(res)

    res = res.get('result')
    if not res:
        return

    descr = res.get('descr')
    odesc = descr.get('order', 'No description available!')
    print(odesc)

    txid = res.get('txid')

    if not txid:
        if args.validate:
            print('NOTICE: validating inputs only. Order not submitted!')
        else:
            print('WARNING: order was NOT successfully added!')
    else:
        for tx in txid:
            print(txid)


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
        print('NOTICE: order(s) is/are pending cancellation!')


def version(args=None):
    """Print program version."""
    print('clikraken version: {}'.format(__version__))


def parse_args():
    """
    Argument parsing

    The client works by giving general options, a subcommand
    and then options specific to the subcommand.

    For example:

        clikraken ticker                    # just a subcommand
        clikraken depth --pair XETHZEUR     # subcommand option
        clikraken --raw olist               # global option
        clikraken place buy 0.1337 10.42    # subcommand argument
    """

    # some help strings that are repeated many times
    pairs_help = "comma delimited list of asset pairs"
    pair_help = "asset pair"

    epilog_str = ("Current default currency pair: {}. Create or edit {} to change it. "
                  "See also the subcommand 'generate_settings'.").format(DEFAULT_PAIR, USER_SETTINGS_PATH)
    parser = argparse.ArgumentParser(
        description='Command line client for the Kraken exchange',
        epilog=epilog_str)
    parser.add_argument('-V', '--version', action='store_const', const=version, dest='main_func',
                        help='show program version')
    parser.add_argument('--raw', action='store_true', help='output raw json results from the API')
    parser.set_defaults(main_func=None)

    subparsers = parser.add_subparsers(dest='subparser_name', help='available subcommands')

    # Generate setting.ini
    parser_gen_settings = subparsers.add_parser(
        'generate_settings',
        help='[clikraken] Output the default settings.ini file',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_gen_settings.set_defaults(sub_func=output_default_settings_ini)

    # ----------
    # Public API
    # ----------

    # Ticker
    parser_ticker = subparsers.add_parser(
        'ticker',
        aliases=['t'],
        help='[public] Get the Ticker',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_ticker.add_argument('-p', '--pair', default=DEFAULT_PAIR,
                               help=pairs_help + " to get info on. ")
    parser_ticker.set_defaults(sub_func=ticker)

    # Market depth (Order book)
    parser_depth = subparsers.add_parser(
        'depth',
        aliases=['d'],
        help='[public] Get the current market depth data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_depth.add_argument('-p', '--pair', default=DEFAULT_PAIR, help=pair_help)
    parser_depth.add_argument('-c', '--count', type=int, default=7, help="maximum number of asks/bids.")
    parser_depth.set_defaults(sub_func=depth)

    # List of last trades
    parser_last_trades = subparsers.add_parser(
        'last_trades',
        aliases=['lt'],
        help='[public] Get the last trades',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_last_trades.add_argument('-p', '--pair', default=DEFAULT_PAIR, help=pair_help)
    parser_last_trades.add_argument('-s', '--since', default=None,
                                    help="return trade data since given idreturn trade data since given id")
    parser_last_trades.add_argument('-c', '--count', type=int, default=15, help="maximum number of trades.")
    parser_last_trades.set_defaults(sub_func=last_trades)

    # -----------
    # Private API
    # -----------

    # User balance
    parser_balance = subparsers.add_parser(
        'balance',
        aliases=['bal'],
        help='[private] Get your current balance',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_balance.set_defaults(sub_func=get_balance)

    # Place an order
    parser_place = subparsers.add_parser(
        'place',
        help='[private] Place an order',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_place.add_argument('type', choices=['sell', 'buy'])
    parser_place.add_argument('volume', type=Decimal)
    parser_place.add_argument('price', default=None, nargs='?')
    parser_place.add_argument('-p', '--pair', default=DEFAULT_PAIR, help=pair_help)
    parser_place.add_argument('-t', '--ordertype', choices=['market', 'limit'], default='limit',
                              help="order type. Currently implemented: [limit, market].")
    parser_place.add_argument('-s', '--starttm', default=0, help="scheduled start time")
    parser_place.add_argument('-e', '--expiretm', default=0, help="expiration time")
    parser_place.add_argument('-q', '--viqc', action='store_true', help="volume in quote currency")
    parser_place.add_argument('-v', '--validate', action='store_true', help="validate inputs only. do not submit order")
    parser_place.set_defaults(sub_func=place_order)

    # cancel an order
    parser_cancel = subparsers.add_parser(
        'cancel',
        aliases=['x'],
        help='[private] Cancel an order',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_cancel.add_argument('order_id', type=str, help="transaction id")
    parser_cancel.set_defaults(sub_func=cancel_order)

    # List of open orders
    parser_olist = subparsers.add_parser(
        'olist',
        aliases=['ol'],
        help='[private] Get a list of your open orders',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_olist.add_argument('-p', '--pair', default=DEFAULT_PAIR, help=pair_help)
    parser_olist.set_defaults(sub_func=list_open_orders)

    # List of closed orders
    parser_clist = subparsers.add_parser(
        'clist',
        aliases=['cl'],
        help='[private] Get a list of your closed orders',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_clist.add_argument('-p', '--pair', default=DEFAULT_PAIR, help=pair_help)
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
