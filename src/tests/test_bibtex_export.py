import os
import unittest
from unittest.mock import Mock, mock_open, patch

from pybtex.database import BibliographyData, Entry

from services.bibtex_export import (create_bib_data, create_bibtex_string,
                                    export_to_bibtex, reference_to_entry)


class TestBibTeXExport(unittest.TestCase):
    def setUp(self):
        self.reference = Mock()
        self.reference.name = "ref1"
        self.reference.get_type.return_value = "article"
        self.reference.get_fields_as_tuples.return_value = [
            ("author", "John Doe"), ("title", "Sample Title")]

        self.reference_manager = Mock()
        self.reference_manager.get_all_references.return_value = [
            self.reference]

    def test_export_to_bibtex(self):
        expected_path = "./exports/bibtex_export.bib"

        with patch("builtins.open", mock_open()) as mock_file, \
                patch("services.bibtex_export.get_full_path", return_value=expected_path):
            path = export_to_bibtex(self.reference_manager)

            mock_file.assert_called_with(path, "w", encoding="utf-8")

        # Normalize paths for cross-platform compatibility
        expected_path = os.path.normpath(expected_path)
        path = os.path.normpath(path)

        self.assertEqual(expected_path, path)

    def test_export_to_bibtex_empty_reference_manager(self):
        expected_path = "./exports/bibtex_export.bib"
        empty_reference_manager = Mock()
        empty_reference_manager.get_all_references.return_value = []

        with patch("builtins.open", mock_open()) as mock_file, \
                patch("services.bibtex_export.get_full_path", return_value=expected_path):
            path = export_to_bibtex(empty_reference_manager)

            mock_file.assert_called_with(path, "w", encoding="utf-8")

        expected_path = os.path.normpath(expected_path)
        path = os.path.normpath(path)

        self.assertEqual(expected_path, path)

    def test_create_bibtex_string(self):
        bibtex_string = create_bibtex_string(self.reference_manager)

        self.assertIn("@article{ref1", bibtex_string)
        self.assertIn('author = "John Doe"', bibtex_string)
        self.assertIn('title = "Sample Title"', bibtex_string)

    def test_create_bib_data_creates_bib_data(self):
        bib_data = create_bib_data(self.reference_manager)

        self.assertIsInstance(bib_data, BibliographyData)

    def test_reference_to_entry_creates_entry(self):
        entry = reference_to_entry(self.reference)

        self.assertIsInstance(entry, Entry)
