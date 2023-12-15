import unittest
from unittest.mock import Mock, patch

from entities.reference import Reference
from services.reference_manager import ReferenceManager
from ui.ui import UI, UserInputError


class TestUi(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = ReferenceManager()
        self.ui = UI(self.manager)

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

        for ref in references:
            self.manager.add(ref)

        with patch("ui.ui.UI.create_type_table") as mock_create_type_table:
            mock_create_type_table.side_effect = ["mocked", "second_mocked"]
            result = self.ui.create_all_tables()
            self.assertIn("mocked", result)

    def test_too_many_extra_fields(self):
        ref_list = [
            Reference("book", {"author": "author", "title": "title",
                               "year": 1, "publisher": "publisher",
                               "extra1": "extra1", "extra2": "extra2",
                               "extra3": "extra3", "extra4": "extra4"})]

        result = self.ui.create_type_table("book", ref_list)
        self.assertNotIn("extra4", result)
        self.assertIn("...", result)

    def test_new_entry(self):
        with patch("ui.ui.create_entry") as mock_create_entry, \
                patch("ui.ui.ReferenceManager.new") as mock_new:
            mock_create_entry.return_value = ("reference key", "fields")
            mock_new.return_value = "reference object"
            result = self.ui.new_entry()

            mock_create_entry.assert_called()
            self.manager.new.assert_called_with("reference key", "fields")
            self.assertEqual(result, ("reference key", "fields"))

    def test_new_entry_using_doi_with_entry(self):
        with patch("ui.ui.create_entry_by_doi") as mock_create_entry, \
                patch("ui.ui.ReferenceManager.new") as mock_new:
            mock_create_entry.side_effect = [("key", "value"), None]
            mock_new.return_value = "reference object"
            result = self.ui.new_entry_using_doi()
            result2 = self.ui.new_entry_using_doi()

        mock_create_entry.assert_called()
        mock_new.assert_called_with("key", "value")
        self.assertEqual(result, ("key", "value"))
        self.assertEqual(result2, None)

    @patch('builtins.input', side_effect=['title', '', ''])
    @patch('builtins.print')
    def test_manager_search_with_valid_input(self, mock_print, mock_input):
        self.ui.manager = Mock()
        self.ui.manager.get_all_fields.return_value = ['title']
        self.ui.manager.search.return_value = ["reference"]
        result = self.ui.manager_search()

        self.ui.manager.get_all_fields.assert_called_once()
        self.ui.manager.search.assert_called_with({})
        mock_input.assert_called()
        mock_print.assert_called_with("Value must not be empty!")
        self.assertEqual(result, ["reference"])

    @patch('builtins.input', side_effect=[''])
    @patch('builtins.print')
    def test_manager_search_empty_input(self, mock_print, mock_input):

        self.ui.manager = Mock()
        self.ui.manager.get_all_fields.return_value = ['title']
        self.ui.manager.search.return_value = []
        result = self.ui.manager_search()

        self.ui.manager.get_all_fields.assert_called_once()
        self.ui.manager.search.assert_called_with({})
        mock_input.assert_called()
        mock_print.assert_called_with('Possible fields: title\n')
        self.assertEqual(result, [])

    @patch('builtins.input', side_effect=['not_title', ''])
    @patch('builtins.print')
    def test_manager_search_with_bad_field(self, mock_print, mock_input):
        self.ui.manager = Mock()
        self.ui.manager.get_all_fields.return_value = ['title']
        self.ui.manager.search.return_value = []
        self.ui.manager_search()

        self.ui.manager.get_all_fields.assert_called_once()
        self.ui.manager.search.assert_called_with({})
        mock_input.assert_called()
        mock_print.assert_called_with(
            "No references with a value for 'not_title'")
