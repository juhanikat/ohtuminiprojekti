import unittest
from unittest.mock import patch

from services.entry_writer import create_entry

entry_writer_path = "services.entry_writer"


class TestCreateEntry(unittest.TestCase):

    @patch(f'{entry_writer_path}.input', create=True)
    def test_complete_entry(self, mock_input):
        mock_input.side_effect = ['book', 'titus',
                                  '2023', 'andy', 'otava', '', 'unittestref']

        expected_citation = 'unittestref'
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

    @patch(f'{entry_writer_path}.input', create=True)
    def test_complete_entry_with_optional_fields(self, mock_input):
        mock_input.side_effect = ['book', 'titus', '2023', 'andy',
                                  'otava', 'volume', 'first edition', '', 'unittestref']

        expected_citation = 'unittestref'
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

    @patch(f'{entry_writer_path}.input', create=True)
    def test_overwriting_written_fields_should_be_blocked(self, mock_input):
        mock_input.side_effect = ['book', 'titus', '2023',
                                  'andy', 'otava', 'author', '', 'unittestref']

        expected_citation = 'unittestref'
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

    @patch(f'{entry_writer_path}.input', create=True)
    def test_can_resume_after_bad_required_field_input(self, mock_input):
        mock_input.side_effect = ['proceedings',
                                  'titus', 'notayear', '2023', '', 'unittestref']

        expected_citation = 'unittestref'
        expected_dict = {
            'entry_type': 'proceedings',
            'title': 'titus',
            'year': '2023'
        }
        expected_result = (expected_citation, expected_dict)

        result = create_entry()
        print(result)
        self.assertEqual(result, expected_result)

    @patch(f'{entry_writer_path}.input', create=True)
    def test_can_abort_at_entry(self, mock_input):
        mock_input.side_effect = ['']

        result = create_entry()
        print(result)
        self.assertFalse(result)

    @patch(f'{entry_writer_path}.input', create=True)
    def test_can_abort_at_required_fields(self, mock_input):
        mock_input.side_effect = ['book', '']

        result = create_entry()
        print(result)
        self.assertFalse(result)

    @patch(f'{entry_writer_path}.input', create=True)
    def test_can_abort_at_citation_key(self, mock_input):
        mock_input.side_effect = ['misc', '', '']

        result = create_entry()
        print(result)
        self.assertFalse(result)

    @patch(f'{entry_writer_path}.input', create=True)
    def test_invalid_entry_type(self, mock_input):
        mock_input.side_effect = ['Idontexist', '']

        result = create_entry()
        print(result)
        self.assertFalse(result)

    @patch(f'{entry_writer_path}.input', create=True)
    def test_invalid_optional_input(self, mock_input):
        mock_input.side_effect = ['misc', 'year', 'badyear', '', 'unittestref']

        expected_citation = 'unittestref'
        expected_dict = {
            'entry_type': 'misc'
        }
        expected_result = (expected_citation, expected_dict)

        result = create_entry()
        print(result)
        self.assertEqual(result, expected_result)

    @patch(f'{entry_writer_path}.input', create=True)
    def test_can_receive_and_use_suggested_citation(self, mock_input):
        mock_input.side_effect = ['proceedings',
                                  'titus', 'notayear', '2023', '', '']

        expected_citation = 'titus-2023'
        expected_dict = {
            'entry_type': 'proceedings',
            'title': 'titus',
            'year': '2023'
        }
        expected_result = (expected_citation, expected_dict)

        result = create_entry()
        print(result)
        self.assertEqual(result, expected_result)

    @patch(f'{entry_writer_path}.input', create=True)
    def test_invalid_citation_key(self, mock_input):
        mock_input.side_effect = [
            'misc', 'year', 'badyear', '', 'I am a space marine', 'unittestref']

        expected_citation = 'unittestref'
        expected_dict = {
            'entry_type': 'misc'
        }
        expected_result = (expected_citation, expected_dict)

        result = create_entry()
        print(result)
        self.assertEqual(result, expected_result)
