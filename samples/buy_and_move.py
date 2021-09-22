#!/usr/bin/env python

"""Script to buy a crypto from another currency and then move the
crypto to a known address. Used to do DCA (Dollar Cost Averaging).

Example to buy 1000€ of BTC and send them to the hw_wallet defined on
Kraken:

$ ./buy_and_move.py 1000 EUR XBT hw_wallet
"""

from decimal import Decimal
import time
import sys

from clikraken.api.api_utils import load_api_keyfile
from clikraken.api.private.get_balance import get_balance
from clikraken.api.private.list_open_orders import list_open_orders
from clikraken.api.private.place_order import place_order
from clikraken.api.private.withdraw import withdraw
from clikraken.api.public.depth import depth
from clikraken.clikraken_utils import load_config

from abstract_automaton import AbstractAutomaton

FEE = Decimal("0.0018")

TRANSFER_FEES = {
    "XBT": Decimal("0.00015"),
}


class DollarCostAveragingAutomaton(AbstractAutomaton):
    state_file = "dca.json"
    decimal_fields = ["amount", "target_amount"]
    seconds_to_wait = 60

    def __init__(self, amount, frm, to, addr):
        self.frm = frm
        self.amount = amount
        self.to = to
        self.addr = addr
        super().__init__()

    def run(self):
        while self.state.startswith("wait_"):
            print("waiting for {}s in {}".format(self.seconds_to_wait, self.state))
            time.sleep(self.seconds_to_wait)
            self.execute_state()

    def init(self, data):
        data["frm"] = self.frm
        data["amount"] = self.amount
        data["to"] = self.to
        data["addr"] = self.addr
        data["pair"] = "X{}Z{}".format(self.to, self.frm)
        self.set_state("wait_for_balance", data)

    def wait_for_balance(self, data):
        bal = get_balance()
        if data["frm"] not in bal:
            print("not", data["frm"], "to buy", data["to"])
        elif bal[data["frm"]] < data["amount"]:
            print(
                "not enough {} ({} < {}) to buy {}".format(
                    data["frm"], bal[data["frm"]], data["amount"], data["to"]
                )
            )
        else:
            self.set_state("buy", data)

    def buy(self, data):
        d = depth(data["pair"], 10)
        asks = d[data["pair"]]["asks"]
        volume = 0
        sum = 0
        for price, vol, _ in asks:
            sum += Decimal(price) * Decimal(vol)
            volume += Decimal(vol)
            if sum > data["amount"]:
                break
        price = sum / volume
        # compute the amount from the current market asks
        # todo(fl) need to take the fees into account
        target_amount = data["amount"] / price
        res = place_order("buy", data["pair"], "market", target_amount)
        txid = res.get("txid")

        if txid:
            data["txid"] = txid[0]
            self.set_state("wait_for_transaction", data)
        else:
            print(res, file=sys.stderr)

    def wait_for_transaction(self, data):
        res = list_open_orders(data["txid"])
        if len(res) == 0:
            self.set_state("transfer", data)
        else:
            print(res, file=sys.stderr)

    def transfer(self, data):
        bal = get_balance()
        if data["to"] not in bal:
            print("no", data["to"], "to send")
        if bal[data["to"]] < data["target_amount"]:
            print("not enough", data["to"], "=>", bal[data["to"]])
        else:
            try:
                fee = TRANSFER_FEES[data["to"]]
                res = withdraw(bal[data["to"]] - fee, data["to"], data["addr"])
                if "refid" in res:
                    data["refid"] = res["refid"]
                    self.set_state("wait_for_transfer", data)
                else:
                    print(res)
            except KeyError:
                print("Unkown fee for {}. Aborting.".format(data["to"]))

    def wait_for_transfer(self, data):
        pass


def main(argv):
    if len(argv) != 5:
        print(
            "Usage: {} <amount to spend> <currency to spend> <currency to buy> <address to move>".format(
                argv[0]
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    load_config()
    load_api_keyfile()

    dca = DollarCostAveragingAutomaton(Decimal(argv[1]), argv[2], argv[3], argv[4])

    dca.run()


if __name__ == "__main__":
    main(sys.argv)

# buy_and_move.py ends here
