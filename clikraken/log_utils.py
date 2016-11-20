# -*- coding: utf8 -*-

"""
clikraken.log_utils

This module sets the logger object up for use throughout clikraken's modules.

Licensed under the Apache License, Version 2.0. See the LICENCE file.
"""

import logging
import os

try:
    import colorlog
    have_colorlog = True
except ImportError:
    colorlog = None
    have_colorlog = False


def setup_logger():
    """Setup a colored logger if available and possible"""

    logger = logging.getLogger('clikraken')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    format_str = '{levelname:8} - {message}'
    f = logging.Formatter(fmt=format_str, style='{')

    if have_colorlog:
        cf = colorlog.ColoredFormatter(fmt='{log_color}' + format_str, style='{')
    else:
        cf = f

    if os.isatty(2):
        ch.setFormatter(cf)
    else:
        ch.setFormatter(f)

    logger.addHandler(ch)

    return logger

logger = setup_logger()
