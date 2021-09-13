# -*- coding: utf-8 -*-

"""
clikraken.clikraken_cmd

This module handles the parsing of the command line arguments
and associates the different subcommands with the corresponding
function to be called.

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

import argparse
import codecs
import importlib
import os
import pkgutil
import textwrap
import sys

import clikraken.global_vars as gv
import clikraken.clikraken_utils as ck_utils


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

    epilog_str = textwrap.dedent(
        """\
        To get help about a subcommand use: clikraken SUBCOMMAND --help
        For example:
            clikraken place --help

        Current default currency pair: {dp}.

        Create or edit the setting file {usp} to change it.
        If the setting file doesn't exist yet, you can create one by doing:
            clikraken generate_settings > {usp}

        You can also set the CLIKRAKEN_DEFAULT_PAIR environment variable
        which has precedence over the settings from the settings file.
        """.format(
            dp=gv.DEFAULT_PAIR, usp=gv.USER_SETTINGS_PATH
        )
    )

    parser = argparse.ArgumentParser(
        description="clikraken - Command line client for the Kraken exchange",
        epilog=epilog_str,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-V",
        "--version",
        action="store_const",
        const=ck_utils.version,
        dest="main_func",
        help="show program version",
    )
    parser.add_argument("--debug", action="store_true", help="debug mode")
    parser.add_argument(
        "--raw", action="store_true", help="output raw json results from the API"
    )
    parser.add_argument(
        "--json", action="store_true", help="output json results from the API"
    )
    parser.add_argument(
        "--csv", action="store_true", help="output results from the API as CSV"
    )
    parser.add_argument(
        "--csvseparator", default=";", help="separator character to use with CSV output"
    )
    parser.add_argument(
        "--cron",
        action="store_true",
        help="activate cron mode (tone down errors due to timeouts or unavailable Kraken service)",
    )
    parser.set_defaults(main_func=None)

    subparsers = parser.add_subparsers(
        dest="subparser_name", help="available subcommands"
    )

    # Generate setting.ini
    parser_gen_settings = subparsers.add_parser(
        "generate_settings",
        help="[clikraken] Print default settings.ini to stdout",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_gen_settings.set_defaults(sub_func=ck_utils.output_default_settings_ini)

    topdir = os.path.dirname(__file__)
    FUNC = "init"
    # load sub-commands dynamically by loading the modules in the
    # api/public and api/private directories calling their init method
    # passing the subparsers variable
    for subdir in ("public", "private"):
        moddir = os.path.join(topdir, "api", subdir)
        for (_, name, _) in pkgutil.iter_modules([moddir]):
            if not name.startswith("_"):
                imported_module = importlib.import_module(
                    "clikraken.api.{}.{}".format(subdir, name)
                )
                if FUNC not in dir(imported_module):
                    print(
                        "Invalid sub-command module {}\n".format(name), file=sys.stderr
                    )
                    continue
                getattr(imported_module, FUNC)(subparsers)

    args = parser.parse_args()

    # make sure that either sub_func or main_func is defined
    # otherwise just print usage and exit
    # (this weird construction is a hack to work around Python bug #9351 https://bugs.python.org/issue9351)
    if all([vars(args).get(f, None) is None for f in ["sub_func", "main_func"]]):
        parser.print_usage()
        sys.exit(os.EX_OK)

    gv.CRON = args.cron

    # Trick from https://stackoverflow.com/a/37059682/862188
    # in order to be able to parse things like "\t" or "\\" for example
    separator = codecs.escape_decode(bytes(args.csvseparator, "utf-8"))[0].decode(
        "utf-8"
    )
    gv.CSV_SEPARATOR = separator

    return args
