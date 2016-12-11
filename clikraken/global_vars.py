# -*- coding: utf8 -*-

"""
clikraken.global_vars

This module serves as a container for global variables.

Licensed under the Apache License, Version 2.0. See the LICENCE file.
"""

import os

# Resolve userpath to an absolute path
DEFAULT_KRAKEN_API_KEYFILE = os.path.expanduser('~/.config/clikraken/kraken.key')
# If the environment variable is set, override the default value
KRAKEN_API_KEYFILE = os.getenv('CLIKRAKEN_API_KEYFILE', DEFAULT_KRAKEN_API_KEYFILE)
KRAKEN_API_KEYFILE = os.path.normpath(KRAKEN_API_KEYFILE)

# Resolve userpath to an absolute path
DEFAULT_USER_SETTINGS_PATH = os.path.expanduser('~/.config/clikraken/settings.ini')
# If the environment variable is set, override the default value
USER_SETTINGS_PATH = os.getenv('CLIKRAKEN_USER_SETTINGS_PATH', DEFAULT_USER_SETTINGS_PATH)
USER_SETTINGS_PATH = os.path.normpath(USER_SETTINGS_PATH)

# Default settings
DEFAULT_SETTINGS_INI = """[clikraken]
# default currency pair when no option '-p' or '--pair' is given
# and the environment variable CLIKRAKEN_DEFAULT_PAIR is not set
currency_pair = XETHZEUR

# Timezone for displaying date and time infos
timezone = Europe/Berlin

# API Trading Agreement
# (change to "agree" after reading https://www.kraken.com/u/settings/api)
trading_agreement = not_agree
"""

# Global variables to be shared between clikraken's modules
KRAKEN_API = None
DEFAULT_PAIR = None
TZ = None
TRADING_AGREEMENT = None
CRON = None
