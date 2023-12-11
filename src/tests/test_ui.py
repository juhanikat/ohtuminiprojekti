import unittest
from unittest.mock import patch

from entities.reference import Reference
from services.reference_manager import ReferenceManager
from ui.ui import UI, UserInputError


class TestUi(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = ReferenceManager()
        self.ui = UI(self.manager)

    def test_listing_references(self):
        result = self.ui.list_all_references()
        self.assertEqual(len(result), 0)
        self.manager.add(Reference("testing"))
        result = self.ui.list_all_references()
        self.assertIn("testing", result)

    @patch("builtins.print")
    @patch("ui.ui.input", create=True)
    def test_listing_empty(self, mock_input, mock_print):
        mock_input.side_effect = ['l']
        self.ui.ask_for_input()
        mock_print.assert_called_with("")

    @patch("builtins.input", create=True)
    def test_changing_file_path_to_empty(self, mock_input):
        mock_input.side_effect = ['f', '']
        self.assertRaises(
            UserInputError, lambda: self.ui.ask_for_input())

    def test_create_type_table(self):
        self.manager.add(
            Reference("book", {"author": "author", "title": "title"}))
        self.manager.add(
            Reference("article", {"author": "author", "title": "title"}))

        references = self.manager.find_by_attribute(
            "entry_type", "book")
        result = self.ui.create_type_table("book", references)
        self.assertIn("book", result)
        self.assertNotIn("article", result)

    def test_create_type_table_max_length(self):
        reference1 = Reference("book", {"title": "title1", "year": 2023,
                                        "author": "Ian Goodfellow, Yoshua Bengio, Aaron Courville",
                                        "publisher": "publisher1"})

        result = self.ui.create_type_table('book', [reference1])

        self.assertIn("Ian Goodfellow, Yoshua Beng...", result)

    def test_create_all_tables(self):
        references = [
            Reference("book", {"entry_type": "book",
                               "author": "author", "title": "title"}),
            Reference("article", {"entry_type": "article",
                                  "author": "author", "title": "title"})
        ]
        # self.manager.add(references[0])
        # self.assertEqual("book", references[0].get_type())

        for ref in references:
            self.manager.add(ref)

        with patch("ui.ui.UI.create_type_table") as mock_create_type_table:
            mock_create_type_table.side_effect = ["mocked", "second_mocked"]
            result = self.ui.create_all_tables()
            self.assertIn("mocked", result)
        # mock_create_type_table.assert_called_with("book", ["title", "year", "author", "publisher"])
