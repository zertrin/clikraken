# -*- coding: utf-8 -*-

"""
"""

from abc import ABC
from decimal import Decimal
import json
import os


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


class AbstractAutomaton(ABC):
    def __init__(self):
        if not getattr(self, "state", False):
            self.state = "init"
        self.load_data()
        self.execute_state()

    def get_state_file(self):
        return os.path.join(os.path.dirname(__file__), self.state_file)

    def load_data(self):
        try:
            with open(self.get_state_file()) as fdinput:
                jdata = json.load(fdinput)
                self._data = jdata["data"]
                self.state = jdata["state"]
            for field in getattr(self, "decimal_fields", []):
                if field in self._data:
                    self._data[field] = Decimal(self._data[field])
        except FileNotFoundError:
            self._data = {}

    def execute_state(self):
        print("Executing state {}".format(self.state))
        getattr(self, self.state)(self._data)

    def set_state(self, new_state, data):
        self._data = data
        self.state = new_state
        with open(self.get_state_file(), "w") as fdoutput:
            json.dump(
                {"state": self.state, "data": self._data}, fdoutput, cls=DecimalEncoder
            )
        self.execute_state()

# abstract_automaton.py ends here
