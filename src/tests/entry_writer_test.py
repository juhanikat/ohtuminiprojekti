import unittest
from unittest.mock import patch
from services.entry_writer import create_entry

class TestCreateEntry(unittest.TestCase):
    @patch('entry_writer.input', create=True)
    def test_complete_entry (self, mock_input):
        mock_input.side_effect = ['validref', 'book', 'andy', 'titus', 'otava', '2023', '']

        expected_citation = 'validref'
        expected_dict = {
            'entry_type': 'book',
            'author': 'andy',
            'title': 'titus',
            'publisher': 'otava',
            'year': '2023'
        }
        expected_result = (expected_citation, expected_dict)

        result = create_entry()
        print(result)
        self.assertEqual(result, expected_result)

    @patch('entry_writer.input', create=True)
    def test_complete_entry_with_optional_fields (self, mock_input):
        mock_input.side_effect = ['validref', 'book', 'andy', 'titus', 'otava', '2023', 'volume', 'first edition', '']

        expected_citation = 'validref'
        expected_dict = {
            'entry_type': 'book',
            'author': 'andy',
            'title': 'titus',
            'publisher': 'otava',
            'year': '2023',
            'volume': 'first edition'
        }
        expected_result = (expected_citation, expected_dict)

        result = create_entry()
        print(result)
        self.assertEqual(result, expected_result)

    @patch('entry_writer.input', create=True)
    def test_overwriting_written_fields_should_be_blocked (self, mock_input):
        mock_input.side_effect = ['validref', 'book', 'andy', 'titus', 'otava', '2023', 'author', '']

        expected_citation = 'validref'
        expected_dict = {
            'entry_type': 'book',
            'author': 'andy',
            'title': 'titus',
            'publisher': 'otava',
            'year': '2023'
        }
        expected_result = (expected_citation, expected_dict)
        
        result = create_entry()
        print(result)
        self.assertEqual(result, expected_result)

    @patch('entry_writer.input', create=True)
    def test_complete_entry_with_empty_required_field (self, mock_input):
        mock_input.side_effect = ['validref', 'book', '']

        result = create_entry()
        self.assertFalse(result)

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