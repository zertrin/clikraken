# -*- coding: utf8 -*-

"""
clikraken.clikraken_cmd

This module handles the parsing of the command line arguments
and associates the different subcommands with the corresponding
function to be called.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import argparse
import textwrap
from decimal import Decimal
import sys

import clikraken.global_vars as gv
import clikraken.clikraken_utils as ck_utils

from clikraken.api.public.depth import depth
from clikraken.api.public.last_trades import last_trades
from clikraken.api.public.ticker import ticker
from clikraken.api.public.asset_pairs import asset_pairs

from clikraken.api.private.cancel_order import cancel_order
from clikraken.api.private.get_balance import get_balance
from clikraken.api.private.list_closed_orders import list_closed_orders
from clikraken.api.private.list_open_orders import list_open_orders
from clikraken.api.private.place_order import place_order


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
        help='[public] Get the Ticker',
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
        aliases=['p'],
        help='[private] Place an order',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_place.add_argument('type', choices=['sell', 'buy'])
    parser_place.add_argument('volume', type=Decimal)
    parser_place.add_argument('price', default=None, nargs='?')
    parser_place.add_argument('-p', '--pair', default=gv.DEFAULT_PAIR, help=pair_help)
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
    parser_olist.set_defaults(sub_func=list_open_orders)

    # List of closed orders
    parser_clist = subparsers.add_parser(
        'clist',
        aliases=['cl'],
        help='[private] Get a list of your closed orders',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_clist.add_argument('-p', '--pair', default=None, help=pair_help)
    parser_clist.set_defaults(sub_func=list_closed_orders)

    args = parser.parse_args()

    # make sure that either sub_func or main_func is defined
    # otherwise just print usage and exit
    # (this weird construction is a hack to work around Python bug #9351 https://bugs.python.org/issue9351)
    if all([vars(args).get(f, None) is None
            for f in ['sub_func', 'main_func']]):
        parser.print_usage()
        sys.exit(0)

    gv.CRON = args.cron

    return args
