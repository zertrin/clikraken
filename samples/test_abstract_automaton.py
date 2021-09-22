from decimal import Decimal
import os
import unittest

from abstract_automaton import AbstractAutomaton


class MyAutomaton(AbstractAutomaton):
    state_file = "my_automaton.json"
    decimal_fields = ["decimal"]

    def __init__(self):
        self.inited = False
        self.state = "myinit"
        super().__init__()

    def myinit(self, data):
        self.inited = True
        data["decimal"] = Decimal("1.3")
        self.set_state("process", data)

    def process(self, data):
        data["decimal"] += 1
        self.set_state("finish", data)

    def finish(self, data):
        pass


class TestAbstractAutomaton(unittest.TestCase):
    def setUp(self):
        self.automaton = MyAutomaton()

    def tearDown(self):
        try:
            os.unlink(self.automaton.get_state_file())
        except FileNotFoundError:
            pass

    def test_init(self):
        self.assertEqual(self.automaton.state, "finish")
        self.assertTrue(self.automaton.inited)
        self.assertEqual(self.automaton._data["decimal"], Decimal("2.3"))
        self.automaton = MyAutomaton()
        self.assertEqual(self.automaton.state, "finish")
        self.assertFalse(self.automaton.inited)


if __name__ == "__main__":
    unittest.main()

# test_abstract_automaton.py ends here
