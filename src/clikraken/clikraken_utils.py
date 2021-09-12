# -*- coding: utf-8 -*-

"""
clikraken.clikraken_utils

This module contains various functions that are used throughout
clikraken's modules.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import arrow
import configparser
import json
import os
from functools import partial

from tabulate import tabulate

import clikraken.global_vars as gv
from clikraken import __version__
from clikraken.log_utils import logger


_tabulate = partial(tabulate, floatfmt=".12g")


def load_config():
    """Load configuration parameters from the settings file"""

    if not os.path.exists(gv.USER_SETTINGS_PATH):
        logger.info(
            "The user settings file {} was not found! "
            "Using hardcoded default values.".format(gv.USER_SETTINGS_PATH)
        )

    config = configparser.ConfigParser()
    config.read_string(gv.DEFAULT_SETTINGS_INI)
    config.read(gv.USER_SETTINGS_PATH)

    conf = config["clikraken"]

    # Get the default currency pair from environment variable if available
    # otherwise take the value from the config file.
    gv.DEFAULT_PAIR = os.getenv("CLIKRAKEN_DEFAULT_PAIR", conf.get("currency_pair"))
    gv.TICKER_PAIRS = os.getenv(
        "CLIKRAKEN_TICKER_PAIRS", conf.get("ticker_currency_pairs")
    )

    # Get the default asset pair from the config file
    gv.DEFAULT_ASSET = os.getenv("CLIKRAKEN_DEFAULT_ASSET", conf.get("asset"))

    gv.TZ = conf.get("timezone")
    gv.TRADING_AGREEMENT = conf.get("trading_agreement")


def version(args=None):
    """Print program version."""
    print("clikraken version: {}".format(__version__))


def humanize_timestamp(ts):
    """Humanize a UNIX timestamp."""
    return arrow.get(ts).humanize()


def format_timestamp(ts):
    """Format a UNIX timestamp to truncated ISO8601 format."""
    return (
        arrow.get(ts).to(gv.TZ).replace(microsecond=0).format("YYYY-MM-DD HH:mm:ssZZ")
    )


def print_results(res):
    """Pretty-print the JSON result from the API."""
    if res is not None:
        print(json.dumps(res, indent=2))


def base_quote_short_from_asset_pair(ap_str):
    """Try to identify the short version of the base and quote of the asset pair"""

    ap_str = ap_str.upper()

    if len(ap_str) == 8:
        # XABCZDEF
        base = ap_str[1:4] if ap_str[0] in ["Z", "X"] else ap_str[:4]
        quote = ap_str[5:] if ap_str[4] in ["Z", "X"] else ap_str[4:]
    elif len(ap_str) == 6:
        # ABCDEF
        base = ap_str[:3]
        quote = ap_str[3:]
    elif len(ap_str) == 7:
        if ap_str[-4] in ["Z", "X"]:
            # ABCXDEF
            base = ap_str[:3]
            quote = ap_str[4:]
        elif ap_str[0] in ["Z", "X"]:
            # XABCDEF
            base = ap_str[1:4]
            quote = ap_str[4:]
        else:
            # ABCDEFG
            # assume EFG is the quote ¯\_(ツ)_/¯
            base = ap_str[:4]
            quote = ap_str[4:]

    return base, quote


def asset_pair_short(ap_str):
    """Convert XETHZEUR to ETHEUR"""
    base, quote = base_quote_short_from_asset_pair(ap_str)
    return base + quote


def check_trading_agreement():
    if gv.TRADING_AGREEMENT != "agree":
        logger.warn(
            "Before being able to use the Kraken API for market orders, "
            "orders that trigger market orders, trailing stop limit orders, and margin orders, "
            "you need to agree to the trading agreement at https://www.kraken.com/u/settings/api "
            'and set the parameter "trading_agreement" to "agree" in the settings file '
            "(located at "
            + gv.USER_SETTINGS_PATH
            + "). If the settings file does not yet exists, "
            "you can generate one by following the instructions in the README.md file."
        )


def output_default_settings_ini(args):
    """Output the contents of the default settings.ini file"""
    print(gv.DEFAULT_SETTINGS_INI)


def csv(items, headers=None):
    output = []
    # Headers
    if headers is not None:
        if headers == "keys":
            headers = items[0].keys()
        output += [headers]
    # Items
    for item in items:
        it = [val for val in item.values()]
        output += [it]
    # Render output as txt
    return "\n".join([(gv.CSV_SEPARATOR).join([str(i) for i in o]) for o in output])
