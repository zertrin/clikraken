#!/usr/bin/env python

'''Script to buy a crypto from another currency and then move the
crypto to a known address. Used to do DCA (Dollar Cost Averaging).

Example to buy 1000€ of BTC and send them to the hw_wallet defined on
Kraken:

$ ./buy_and_move.py 1000 EUR XBT hw_wallet
'''

from decimal import Decimal
import sys

from clikraken.api.api_utils import load_api_keyfile
from clikraken.api.private.get_balance import get_balance
from clikraken.api.private.place_order import place_order
from clikraken.api.public.depth import depth
from clikraken.clikraken_utils import load_config


def main(argv):
    if len(argv) != 5:
        print("Usage: {} <amount to spend> <currency to spend> <currency to buy> <address to move>".format(argv[0]),
              file=sys.stderr)
        sys.exit(1)
    frm = argv[1]
    amount = Decimal(argv[2])
    to = argv[3]
    addr = argv[4]

    pair = "X{}Z{}".format(to, frm)

    load_config()
    load_api_keyfile()

    bal = get_balance()

    if frm in bal:
        print("From:", bal[frm], frm)
        if bal[frm] < amount:
            print("not enough", frm, "to buy", to)
        else:
            d = depth(pair, 10)
            asks = d[pair]["asks"]
            volume = 0
            sum = 0
            for price, vol, _ in asks:
                sum += Decimal(price) * Decimal(vol)
                volume += Decimal(vol)
            price = sum / volume
            # compute the amount from the current market asks
            # todo(fl) need to take the fees into account
            target_amount = amount / price
            res = place_order("buy", pair, "market", target_amount, validate=True)
            print(res)
            # todo(fl) wait for the order to be fulfilled and transfer
            # the crypto to the wallet


if __name__ == "__main__":
    main(sys.argv)

# buy_and_move.py ends here
