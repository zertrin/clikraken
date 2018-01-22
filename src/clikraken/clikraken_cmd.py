# -*- coding: utf8 -*-

"""
clikraken.clikraken_cmd

This module handles the parsing of the command line arguments
and associates the different subcommands with the corresponding
function to be called.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import argparse
import codecs
import textwrap
from decimal import Decimal
import sys

import clikraken.global_vars as gv
import clikraken.clikraken_utils as ck_utils

from clikraken.api.public.asset_pairs import asset_pairs
from clikraken.api.public.depth import depth
from clikraken.api.public.last_trades import last_trades
from clikraken.api.public.ticker import ticker
from clikraken.api.public.ohlc import ohlc

from clikraken.api.private.cancel_order import cancel_order
from clikraken.api.private.get_balance import get_balance
from clikraken.api.private.get_deposit_addresses import get_deposit_addresses
from clikraken.api.private.get_deposit_methods import get_deposit_methods
from clikraken.api.private.get_ledgers import get_ledgers
from clikraken.api.private.get_trade_balance import get_trade_balance
from clikraken.api.private.list_closed_orders import list_closed_orders
from clikraken.api.private.list_open_orders import list_open_orders
from clikraken.api.private.list_open_positions import list_open_positions
from clikraken.api.private.place_order import place_order
from clikraken.api.private.trades import trades


def parse_args():
    """
    Argument parsing

    The client works by giving general options, a subcommand
    and then options specific to the subcommand.

    For example:

        clikraken ticker                    # just a subcommand
        clikraken depth --pair XETHZEUR     # subcommand option
        clikraken ohlc -i 15 -s 1508513700
        clikraken --raw olist               # global option
        clikraken place buy 0.1337 10.42    # subcommand argument
    """

    # some help strings that are repeated many times
    pairs_help = "comma delimited list of asset pairs"
    pair_help = "asset pair"

    epilog_str = textwrap.dedent("""\
        To get help about a subcommand use: clikraken SUBCOMMAND --help
        For example:
            clikraken place --help

        Current default currency pair: {dp}.

        Create or edit the setting file {usp} to change it.
        If the setting file doesn't exist yet, you can create one by doing:
            clikraken generate_settings > {usp}

        You can also set the CLIKRAKEN_DEFAULT_PAIR environment variable
        which has precedence over the settings from the settings file.
        """.format(dp=gv.DEFAULT_PAIR, usp=gv.USER_SETTINGS_PATH))

    parser = argparse.ArgumentParser(
        description='clikraken - Command line client for the Kraken exchange',
        epilog=epilog_str,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-V', '--version', action='store_const', const=ck_utils.version, dest='main_func',
                        help='show program version')
    parser.add_argument('--debug', action='store_true', help='debug mode')
    parser.add_argument('--raw', action='store_true', help='output raw json results from the API')
    parser.add_argument('--csv', action='store_true', help='output results from the API as CSV')
    parser.add_argument('--csvseparator', default=';', help='separator character to use with CSV output')
    parser.add_argument('--cron', action='store_true',
                        help='activate cron mode (tone down errors due to timeouts or unavailable Kraken service)')
    parser.set_defaults(main_func=None)

    subparsers = parser.add_subparsers(dest='subparser_name', help='available subcommands')

    # Generate setting.ini
    parser_gen_settings = subparsers.add_parser(
        'generate_settings',
        help='[clikraken] Print default settings.ini to stdout',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_gen_settings.set_defaults(sub_func=ck_utils.output_default_settings_ini)

    # ----------
    # Public API
    # ----------

    # Asset Pairs
    parser_asset_pairs = subparsers.add_parser(
        'asset_pairs',
        aliases=['ap'],
        help='[public] Get the list of available asset pairs',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_asset_pairs.set_defaults(sub_func=asset_pairs)

    # Ticker
    parser_ticker = subparsers.add_parser(
        'ticker',
        aliases=['t'],
        help='[public] Get the ticker',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_ticker.add_argument('-p', '--pair', default=gv.TICKER_PAIRS,
                               help=pairs_help + " to get info on. ")
    parser_ticker.set_defaults(sub_func=ticker)

    # Market depth (Order book)
    parser_depth = subparsers.add_parser(
        'depth',
        aliases=['d'],
        help='[public] Get the current market depth data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_depth.add_argument('-p', '--pair', default=gv.DEFAULT_PAIR, help=pair_help)
    parser_depth.add_argument('-c', '--count', type=int, default=7, help="maximum number of asks/bids.")
    parser_depth.set_defaults(sub_func=depth)

    # List of last trades
    parser_last_trades = subparsers.add_parser(
        'last_trades',
        aliases=['lt'],
        help='[public] Get the last trades',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_last_trades.add_argument('-p', '--pair', default=gv.DEFAULT_PAIR, help=pair_help)
    parser_last_trades.add_argument('-s', '--since', default=None,
                                    help="return trade data since given id")
    parser_last_trades.add_argument('-c', '--count', type=int, default=15, help="maximum number of trades.")
    parser_last_trades.set_defaults(sub_func=last_trades)

    # Open High Low Close data
    parser_ohlc = subparsers.add_parser(
        'ohlc',
        aliases=['oh'],
        help='[public] Get the ohlc data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_ohlc.add_argument(
        '-p', '--pair', default=gv.DEFAULT_PAIR, help=pair_help)
    parser_ohlc.add_argument(
        '-i', '--interval', default=1,
        help="return ohlc data for interval in minutes; 1, 5, 15, 30, 60, 240, 1440, 10800, 21600.")
    parser_ohlc.add_argument('-s', '--since', default=None,
                             help="return ohlc data since given id")
    parser_ohlc.add_argument('-c', '--count', type=int,
                             default=50, help="maximum number of intervals.")
    parser_ohlc.set_defaults(sub_func=ohlc)

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

    # User trade balance
    parser_trade_balance = subparsers.add_parser(
        'trade_balance',
        aliases=['tbal'],
        help='[private] Get your current trade balance',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_trade_balance.set_defaults(sub_func=get_trade_balance)

    # Place an order
    parser_place = subparsers.add_parser(
        'place',
        aliases=['p'],
        help='[private] Place an order',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_place.add_argument('type', choices=['sell', 'buy'])
    parser_place.add_argument('volume', type=Decimal)
    parser_place.add_argument('price', default=None, nargs='?')
    parser_place.add_argument('-l', '--leverage', default="none", help='leverage for margin trading')
    parser_place.add_argument('-p', '--pair', default=gv.DEFAULT_PAIR, help=pair_help)
    parser_place.add_argument('-t', '--ordertype', choices=['market', 'limit'], default='limit',
                              help="order type. Currently implemented: [limit, market].")
    parser_place.add_argument('-s', '--starttm', default=0, help="scheduled start time")
    parser_place.add_argument('-e', '--expiretm', default=0, help="expiration time")
    parser_place.add_argument('-r', '--userref', help="user reference id.  32-bit signed number.  (optional)")
    parser_place.add_argument('-q', '--viqc', action='store_true', help="volume in quote currency")
    parser_place.add_argument('-T', '--nopost', action='store_true',
                              help="disable 'post-only' option (for limit taker orders)")
    parser_place.add_argument('-v', '--validate', action='store_true', help="validate inputs only. do not submit order")
    parser_place.set_defaults(sub_func=place_order)

    # cancel an order
    parser_cancel = subparsers.add_parser(
        'cancel',
        aliases=['x'],
        help='[private] Cancel orders',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_cancel.add_argument('order_ids', type=str, nargs='+', help="transaction ids")
    parser_cancel.set_defaults(sub_func=cancel_order)

    # List of open orders
    parser_olist = subparsers.add_parser(
        'olist',
        aliases=['ol'],
        help='[private] Get a list of your open orders',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_olist.add_argument('-p', '--pair', default=None, help=pair_help)
    parser_olist.add_argument('-i', '--txid', default=None,
                              help='comma delimited list of transaction ids to query info about (20 maximum)')
    parser_olist.set_defaults(sub_func=list_open_orders)

    # List of open positions
    parser_oplist = subparsers.add_parser(
        'positions',
        aliases=['pos'],
        help='[private] Get a list of your open positions',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_oplist.set_defaults(sub_func=list_open_positions)

    # List of closed orders
    parser_clist = subparsers.add_parser(
        'clist',
        aliases=['cl'],
        help='[private] Get a list of your closed orders',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_clist.add_argument('-p', '--pair', default=None, help=pair_help)
    parser_clist.add_argument('-i', '--txid', default=None,
                              help='comma delimited list of transaction ids to query info about (20 maximum)')
    parser_clist.set_defaults(sub_func=list_closed_orders)

    # Get ledgers info
    parser_ledgers = subparsers.add_parser(
        'ledgers',
        aliases=['lg'],
        help='[private] Get ledgers info',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_ledgers.add_argument(
        '-a', '--asset',
        default='all',
        help='comma delimited list of assets to restrict output to')
    parser_ledgers.add_argument(
        '-t', '--type',
        default='all',
        help='type of ledger to retrieve. Possible values: all|deposit|withdrawal|trade|margin')
    parser_ledgers.add_argument(
        '-s', '--start',
        default=None,
        help='starting unix timestamp or ledger id of results (exclusive)')
    parser_ledgers.add_argument(
        '-e', '--end',
        default=None,
        help='ending unix timestamp or ledger id of results (exclusive)')
    parser_ledgers.add_argument(
        '-o', '--ofs',
        default=None,
        help='result offset')
    parser_ledgers.add_argument(
        '-i', '--id',
        default=None,
        help='comma delimited list of ledger ids to query info about (20 maximum)')
    parser_ledgers.set_defaults(sub_func=get_ledgers)

    # Get trades info
    parser_trades = subparsers.add_parser(
        'trades',
        aliases=['tr'],
        help='[private] Get trades history',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_trades.add_argument(
        '-t', '--type',
        default='all',
        help='type of trade. Values: all|any position|closed position|closing position|no position')
    # TODO: trades parameter
    parser_trades.add_argument(
        '-s', '--start',
        default=None,
        help='starting unix timestamp or trade tx id of results (exclusive)')
    parser_trades.add_argument(
        '-e', '--end',
        default=None,
        help='ending unix timestamp or trade tx id of results (exclusive)')
    parser_trades.add_argument(
        '-o', '--ofs',
        default=None,
        help='result offset')
    parser_trades.add_argument(
        '-i', '--id',
        default=None,
        help='comma delimited list of transaction ids to query info about (20 maximum)')
    parser_trades.add_argument('-p', '--pair', default=None, help=pair_help)
    parser_trades.set_defaults(sub_func=trades)

    # User Funding

    # Deposit Methods
    parser_deposit_methods = subparsers.add_parser(
        'deposit_methods',
        aliases=['dm'],
        help='[private] Get deposit methods',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_deposit_methods.add_argument('-a', '--asset', default=gv.DEFAULT_ASSET, help='asset being deposited')
    parser_deposit_methods.set_defaults(sub_func=get_deposit_methods)

    # Deposit Addresses
    parser_deposit_addresses = subparsers.add_parser(
        'deposit_addresses',
        aliases=['da'],
        help='[private] Get deposit addresses',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_deposit_addresses.add_argument('-a', '--asset', default=gv.DEFAULT_ASSET, help='asset being deposited')
    parser_deposit_addresses.add_argument('-m', '--method', default=None, help='name of the deposit method')
    parser_deposit_addresses.add_argument('-n', '--new', action='store_true',
                                          help="whether or not to generate a new address")
    parser_deposit_addresses.add_argument('-1', '--one', action='store_true', help="return just one address")
    parser_deposit_addresses.set_defaults(sub_func=get_deposit_addresses)

    args = parser.parse_args()

    # make sure that either sub_func or main_func is defined
    # otherwise just print usage and exit
    # (this weird construction is a hack to work around Python bug #9351 https://bugs.python.org/issue9351)
    if all([vars(args).get(f, None) is None
            for f in ['sub_func', 'main_func']]):
        parser.print_usage()
        sys.exit(0)

    gv.CRON = args.cron

    # Trick from https://stackoverflow.com/a/37059682/862188
    # in order to be able to parse things like "\t" or "\\" for example
    separator = codecs.escape_decode(bytes(args.csvseparator, "utf-8"))[0].decode("utf-8")
    gv.CSV_SEPARATOR = separator

    return args
