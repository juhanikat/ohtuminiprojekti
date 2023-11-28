import unittest

from ui.ui import list_all_references, change_file_path, new_entry, UserInputError
from services.reference_manager import ReferenceManager
from entities.reference import Reference


class TestUi(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = ReferenceManager()

    def test_listing_references(self):
        result = list_all_references(self.manager)
        self.assertEqual(len(result), 0)
        self.manager.add(Reference("testing"))
        result = list_all_references(self.manager)
        self.assertIn("testing", result)

    def test_change_file_path_to_empty_string(self):
        change_file_path(self.manager, "", "test.json")
        self.assertRaises(UserInputError)
