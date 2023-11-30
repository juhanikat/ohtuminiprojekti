import unittest
from unittest.mock import patch
from ui.ui import UI, UserInputError
from services.reference_manager import ReferenceManager
from stub_io import StubIO
from entities.reference import Reference


class TestUi(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = ReferenceManager()
        self.io = StubIO()
        self.ui = UI(self.manager, self.io)

    def test_listing_references(self):
        result = self.ui.list_all_references()
        self.assertEqual(len(result), 0)
        self.manager.add(Reference("testing"))
        result = self.ui.list_all_references()
        self.assertIn("testing", result)

    @patch("stub_io.StubIO.write")
    @patch("ui.ui.input", create=True)
    def test_listing_empty(self, mock_input, mock_print):
        mock_input.side_effect = ['l']
        self.ui.ask_for_input()
        mock_print.assert_called_with("")

    @patch("stub_io.StubIO.read", create=True)
    def test_changing_file_path_to_empty(self, mock_input):
        mock_input.side_effect = ['f', '']
        self.assertRaises(
            UserInputError, lambda: self.ui.ask_for_input())
