import unittest
from unittest.mock import patch
from entities.reference import Reference


class TestReference(unittest.TestCase):
    def test_get_type_with_entry_type(self):
        obj = Reference("ref_name", {"entry_type": "type1"})
        self.assertEqual(obj.get_type(), 'type1')

    def test_get_type_without_entry_type(self):
        obj = Reference("ref_name")
        self.assertIsNone(obj.get_type())

    def test_remove_field(self):
        obj = Reference(
            "ref_name", {"entry_type": "type1", "field1": "value1"})
        obj.remove_field("field1")
        self.assertNotIn("field1", obj.fields)

    def test_str_(self):
        obj = Reference(
            "ref_name", {"entry_type": "type1", "field1": "value1"})
        self.assertEqual(
            str(obj), "ref_name (Entry_type: type1, Field1: value1)")
