import unittest
from unittest.mock import patch

from services.doi_fetcher import create_entry_by_doi, parse_field

doi_path = "services.doi_fetcher"

class TestDOI(unittest.TestCase):
    @patch(f'{doi_path}.create_citation_key')
    @patch(f'{doi_path}.retrieve_data_from_database')
    @patch(f'{doi_path}.input', create=True)
    def test_fetch_data_book(self, mock_input, mock_retrieve, mock_citation_key):
        mock_input.side_effect = ['asd', '']

        mock_citation_key.return_value = "mockkey"
        mock_retrieve.return_value = {
            'type': 'book',
            'title': ['keittokirja'],
            'issued': {'date-parts': [[2023]]},
            'author': [{'given': 'tony', 'family': 'montana'}],
            'publisher': 'otava',
        }

        expected_citation = 'mockkey'
        expected_dict = {
            'entry_type': 'book',
            'author': 'tony montana',
            'title': 'keittokirja',
            'publisher': 'otava',
            'year': '2023'
        }

        expected_result = (expected_citation, expected_dict)
        result = create_entry_by_doi()
        self.assertEqual(result, expected_result)

    @patch(f'{doi_path}.create_citation_key')
    @patch(f'{doi_path}.retrieve_data_from_database')
    @patch(f'{doi_path}.input', create=True)
    def test_fetch_data_book_convert_editors_into_authors (self, mock_input, mock_retrieve, mock_citation_key):
        mock_input.side_effect = ['asd', '']

        mock_citation_key.return_value = "mockkey"
        mock_retrieve.return_value = {
            'type': 'book',
            'title': ['keittokirja'],
            'issued': {'date-parts': [[2023]]},
            'editor': [{'given': 'tony', 'family': 'montana'}],
            'publisher': 'otava',
        }

        expected_citation = 'mockkey'
        expected_dict = {
            'entry_type': 'book',
            'author': 'tony montana',
            'title': 'keittokirja',
            'publisher': 'otava',
            'year': '2023'
        }

        expected_result = (expected_citation, expected_dict)
        result = create_entry_by_doi()
        self.assertEqual(result, expected_result)

    @patch(f'{doi_path}.input', create=True)
    def test_can_abort_immediately (self, mock_input):
        mock_input.side_effect = ['']

        result = create_entry_by_doi()
        self.assertFalse(result)

    def test_parse_journal(self):
        test_data = {
            'type': 'article',
            'journal': 'MIT',
        }

        before_dict = {
            'entry_type': 'article',
        }

        after_dict = {
            'entry_type': 'article',
            'journal': 'MIT',
        }

        parse_field("journal", before_dict, "article", test_data)
        self.assertEqual(before_dict, after_dict)

    def test_parse_pages(self):
        test_data = {
            'type': 'inbook',
            'page': '50',
        }

        before_dict = {
            'entry_type': 'inbook',
        }

        after_dict = {
            'entry_type': 'inbook',
            'pages': '50',
        }

        parse_field("pages", before_dict, "inbook", test_data)
        self.assertEqual(before_dict, after_dict)