# -*- coding: utf8 -*-

"""
clikraken.api.api_utils

This module contains various functions related to interacting
with or processing data from Kraken's API.

Licensed under the Apache License, Version 2.0. See the LICENCE file.
"""

import socket
from collections import OrderedDict

import krakenex
import os

import clikraken.global_vars as gv
from clikraken.clikraken_utils import format_timestamp
from clikraken.log_utils import logger


def load_api_keyfile():
    """Load the Kraken API keyfile"""

    if not os.path.exists(gv.KRAKEN_API_KEYFILE):
        logger.error("The API keyfile {} was not found! Aborting...".format(gv.KRAKEN_API_KEYFILE))
        exit(2)

    # Instanciate the krakenex module to communicate with Kraken's API
    gv.KRAKEN_API = krakenex.API()

    # Load the API key of the user
    gv.KRAKEN_API.load_key(gv.KRAKEN_API_KEYFILE)


def query_api(api_type, *args):
    """
    Wrapper to query Kraken's API through krakenex
    and handle connection errors.
    """

    # default to empty dict because that's the expected return type
    res = {}

    # just a mapping from api_type to the function to be called
    api_func = {
        'public': gv.KRAKEN_API.query_public,
        'private': gv.KRAKEN_API.query_private
    }
    # select the appropriate method depending on the api_type string
    func = api_func.get(api_type)

    if func is not None:
        try:
            # call to the krakenex API
            res = func(*args)
        except (socket.timeout, socket.error, ConnectionError, TimeoutError) as e:
            # if cron mode is active, tone down timeout errors in order to not raise too many
            # cron emails when Kraken is temporarily not available
            if gv.CRON:
                log = logger.info
            else:
                log = logger.error
            log('Network error while querying Kraken API!')
            log(repr(e))
        except ValueError:
            if gv.CRON:
                pass
            else:
                logger.exception('ValueError while querying Kraken API!')
        except Exception:
            logger.exception('Exception while querying Kraken API!')

    err = res.get('error', [])
    for e in err:
        # if cron mode is active, tone down some Kraken errors in order to not raise too many
        # cron emails when Kraken is temporarily not available
        if gv.CRON and e in ['EService:Unavailable']:
            log = logger.info
        else:
            log = logger.error
        log('{}'.format(e))

    return res


def parse_order_res(in_ol, status_list_filter=None):
    """
    Helper to parse the order results from the API.

    Depending on the status of the orders, different
    properties are available.

    See Kraken's API documentation for details.
    """

    # we will store the buy and sell orders separately during parsing
    ol = {'buy': [], 'sell': []}

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
