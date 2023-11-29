import unittest
from unittest.mock import patch
from ui.ui import list_all_references, change_file_path, new_entry, ask_for_input, UserInputError
from services.reference_manager import ReferenceManager
from entities.reference import Reference


class TestUi(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = ReferenceManager()

    def test_listing_references(self):
        result = list_all_references(self.manager)
        self.assertEqual(len(result), 0)
        self.manager.add(Reference("testing"))
        result = list_all_references(self.manager)
        self.assertIn("testing", result)

    def test_change_file_path_to_empty_string(self):
        change_file_path(self.manager, "", "test.json")
        self.assertRaises(UserInputError)

    @patch("builtins.print")
    @patch("ui.ui.input", create=True)
    def test_listing_empty(self, mock_input, mock_print):
        mock_input.side_effect = ['l']
        ask_for_input(self.manager)
        mock_print.assert_called_with()
