# -*- coding: utf8 -*-

"""
clikraken.log_utils

This module sets the logger object up for use throughout clikraken's modules.

Licensed under the Apache License, Version 2.0. See the LICENCE file.
"""

import logging
import os
import sys

# fix issues with Unicode chars on Windows console
try:
    import win_unicode_console
except ImportError:
    pass
else:
    win_unicode_console.enable()

try:
    import colorlog
    have_colorlog = True
except ImportError:
    colorlog = None
    have_colorlog = False


class LessThanFilter(logging.Filter):
    """Custom logging filter letting LogRecord pass only if their level is below a limit"""

    def __init__(self, exclusive_maximum, name=""):
        super(LessThanFilter, self).__init__(name)
        self.max_level = exclusive_maximum

    def filter(self, record):
        # non-zero return means we log this message
        return record.levelno < self.max_level


def setup_logger():
    """Setup a colored logger if available and possible"""

    logger = logging.getLogger('clikraken')
    logger.setLevel(logging.DEBUG)

    # log to stdout from DEBUG to INFO
    ch_out = logging.StreamHandler(sys.stdout)
    ch_out.setLevel(logging.DEBUG)
    ch_out.addFilter(LessThanFilter(logging.WARNING))

    # WARNING and above goes to stderr
    ch_err = logging.StreamHandler(sys.stderr)
    ch_err.setLevel(logging.WARNING)

    format_str = '{levelname:8} - {message}'

    # basic formatter
    f = logging.Formatter(fmt=format_str, style='{')

    # colored formatted
    if have_colorlog:
        cf = colorlog.ColoredFormatter(fmt='{log_color}' + format_str, style='{')
    else:
        cf = f

    # only use the colored formatter when we are outputting to a terminal
    if os.isatty(2):
        ch_out.setFormatter(cf)
        ch_err.setFormatter(cf)
    else:
        ch_out.setFormatter(f)
        ch_err.setFormatter(f)

    logger.addHandler(ch_out)
    logger.addHandler(ch_err)

    return logger

logger = setup_logger()
