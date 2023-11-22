import unittest
from unittest.mock import patch
from entry_writer import create_entry

class TestCreateEntry(unittest.TestCase):
    @patch('entry_writer.input', create=True)
    def test_complete_entry (self, mock_input):
        mock_input.side_effect = ['validkey', 'article', 'author', 'andy', 'title', 'titus', 'year', '2023', '']

        expected = {
            'citation': 'validkey',
            'entry_type': 'article',
            'author': 'andy',
            'title': 'titus',
            'year': '2023'
        }
        result = create_entry()
        print(result)
        self.assertEqual(result, expected)

    @patch('entry_writer.input', create=True)
    def test_empty_citation (self, mock_input):
        mock_input.side_effect=['', 'article', 'author', 'andy', 'title', 'titus', 'year', '2023', '']

        result = create_entry()
        print(result)
        self.assertFalse(result)

    @patch('entry_writer.input', create=True)
    def test_empty_entry_type (self, mock_input):
        mock_input.side_effect=['validkey', '', 'author', 'andy', 'title', 'titus', 'year', '2023', '']

        result = create_entry()
        print(result)
        self.assertFalse(result)