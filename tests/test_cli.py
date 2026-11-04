import unittest

from mindreader.bots import all_bots
from mindreader.cli import DEFAULT_BOT, MENU_ORDER, _menu_order, resolve_bot_choice


class MenuOrderTest(unittest.TestCase):
    def test_starter_bots_come_first_and_every_bot_is_included(self):
        bots = all_bots()
        ordered = _menu_order(bots)
        starter = [bot_id for bot_id in MENU_ORDER if bot_id in bots]
        self.assertEqual(ordered[:len(starter)], starter)
        self.assertEqual(set(ordered), set(bots))
        self.assertEqual(len(ordered), len(bots))


class ResolveBotChoiceTest(unittest.TestCase):
    def setUp(self):
        bots = all_bots()
        self.bots = {bot_id: bots[bot_id] for bot_id in _menu_order(bots)}

    def test_empty_choice_uses_default(self):
        self.assertEqual(resolve_bot_choice("", self.bots, DEFAULT_BOT), DEFAULT_BOT)
        self.assertEqual(resolve_bot_choice("   ", self.bots, DEFAULT_BOT), DEFAULT_BOT)

    def test_number_selects_the_matching_bot(self):
        first_id = list(self.bots)[0]
        self.assertEqual(resolve_bot_choice("1", self.bots, DEFAULT_BOT), first_id)

    def test_bot_id_and_name_are_case_insensitive(self):
        self.assertEqual(resolve_bot_choice("frequency", self.bots, DEFAULT_BOT), "frequency")
        self.assertEqual(resolve_bot_choice("FREQUENCY", self.bots, DEFAULT_BOT), "frequency")
        self.assertEqual(resolve_bot_choice("The Accountant", self.bots, DEFAULT_BOT), "frequency")

    def test_invalid_choices_return_none(self):
        self.assertIsNone(resolve_bot_choice("banana", self.bots, DEFAULT_BOT))
        self.assertIsNone(resolve_bot_choice("99", self.bots, DEFAULT_BOT))


if __name__ == "__main__":
    unittest.main()
