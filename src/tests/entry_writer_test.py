import unittest
from unittest.mock import patch
from entry_writer import create_entry

class TestCreateEntry(unittest.TestCase):
    @patch('entry_writer.input', create=True)
    def test_complete_entry (self, mock_input):
        mock_input.side_effect = ['validref', 'book', 'andy', 'titus', 'otava', '2023', '']

        expected = {
            'citation': 'validref',
            'entry_type': 'book',
            'author': 'andy',
            'title': 'titus',
            'publisher': 'otava',
            'year': '2023'
        }
        result = create_entry()
        print(result)
        self.assertEqual(result, expected)

    @patch('entry_writer.input', create=True)
    def test_complete_entry_with_optional_fields (self, mock_input):
        mock_input.side_effect = ['validref', 'book', 'andy', 'titus', 'otava', '2023', 'volume', 'first edition', '']

        expected = {
            'citation': 'validref',
            'entry_type': 'book',
            'author': 'andy',
            'title': 'titus',
            'publisher': 'otava',
            'year': '2023',
            'volume': 'first edition'
        }
        result = create_entry()
        print(result)
        self.assertEqual(result, expected)

    @patch('entry_writer.input', create=True)
    def test_invalid_citation (self, mock_input):
        mock_input.side_effect=['']

        result = create_entry()
        print(result)
        self.assertFalse(result)

    @patch('entry_writer.input', create=True)
    def test_invalid_entry_type (self, mock_input):
        mock_input.side_effect=['validref', 'Idontexist']

        result = create_entry()
        print(result)
        self.assertFalse(result)