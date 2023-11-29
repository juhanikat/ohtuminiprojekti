import unittest
from unittest.mock import patch
from bibtex_utils import ask_fields, get_reference_type


class TestReferenceFields(unittest.TestCase):

    @patch('builtins.input', side_effect=['article'])
    def test_get_reference_valid(self, mock_input):
        result = get_reference_type()
        self.assertEqual(result, 'article')

    @patch('builtins.input', side_effect=['invalid', 'article'])
    def test_get_reference_invalid_then_valid(self, mock_input):
        result = get_reference_type()
        self.assertEqual(result, 'article')

    @patch('builtins.input', side_effect=['exit'])
    def test_get_reference_type_exit(self, mock_input):
        result = get_reference_type()
        self.assertIsNone(result)

    @patch('builtins.input', side_effect=['key', 'Jaska', 'Lunta sataa', 'Lehti', '2023', '2'])
    def test_ask_fields_article(self, mock_input):
        reference_type = 'article'
        result = ask_fields(reference_type)
        expected_result = ('key', {'author': 'Jaska', 'title': 'Lunta sataa',
                           'journal': 'Lehti', 'year': '2023', 'volume': '2'})
        self.assertEqual(result, expected_result)

    @patch('builtins.input', side_effect=['key', 'Jaska', 'Lunta sataa', 'Kirjat', '2023'])
    def test_ask_fields_book(self, mock_input):
        reference_type = 'book'
        result = ask_fields(reference_type)
        expected_result = ('key', {
                           'author': 'Jaska', 'title': 'Lunta sataa', 'publisher': 'Kirjat', 'year': '2023'})
        self.assertEqual(result, expected_result)

    @patch('builtins.input', side_effect=['key', 'Jaska', 'Lunta sataa', 'Otsikko', '2023'])
    def test_ask_fields_inproceedings(self, mock_input):
        reference_type = 'inproceedings'
        result = ask_fields(reference_type)
        expected_result = ('key', {
                           'author': 'Jaska', 'title': 'Lunta sataa', 'booktitle': 'Otsikko', 'year': '2023'})
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
