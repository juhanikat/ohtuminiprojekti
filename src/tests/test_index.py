import unittest

from index import list_all_references
from services.reference_manager import ReferenceManager
from entities.reference import Reference


class TestIndex(unittest.TestCase):

    def test_listing_references(self):
        manager = ReferenceManager()
        result = list_all_references(manager)
        self.assertEqual(len(result), 0)
        manager.Add(Reference("testing"))
        result = list_all_references(manager)
        self.assertIn("testing", result)
