#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
clikraken

Command line client for the Kraken exchange

Licensed under the Apache License, Version 2.0. See the LICENSE file.
"""

from clikraken.api.api_utils import load_api_keyfile
from clikraken.clikraken_cmd import parse_args
from clikraken.clikraken_utils import load_config


def main():
    """Entrypoint for clikraken"""

    load_config()
    load_api_keyfile()

    # parse arguments
    args = parse_args()

    # args.sub_func contains the function to be called
    # depending on the chosen subcommand. If no subcomand
    # is called, then use the function given by args.main_func
    func = args.sub_func if 'sub_func' in args else args.main_func

    if callable(func):
        func(args)
