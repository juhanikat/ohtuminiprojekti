import unittest
from entities.reference import Reference
from services.reference_manager import ReferenceManager


class TestReferenceManager(unittest.TestCase):
    def setUp(self):
        self.rm = ReferenceManager()

    def test_new_reference(self):
        self.rm.new("TestReference")
        self.assertEqual(len(self.rm.get_all_references()), 1)

    def test_add_reference(self):
        reference = Reference("TestReference")
        self.rm.add(reference)
        self.assertEqual(len(self.rm.get_all_references()), 1)

    def test_add_duplicate_reference(self):
        reference1 = Reference("TestReference")
        reference2 = Reference("TestReference")

        self.rm.add(reference1)

        with self.assertRaises(ValueError):
            self.rm.add(reference2)

    def test_edit_reference(self):
        self.rm.new("TestReference", {"field1": "value1"})
        result = self.rm.edit("TestReference", "field1", "new_value")
        self.assertTrue(result)
        self.assertEqual(self.rm.find_by_name(
            "TestReference").fields["field1"], "new_value")

    def test_edit_nonexistent_reference(self):
        result = self.rm.edit("NonexistentReference", "field1", "new_value")
        self.assertFalse(result)

    def test_find_by_name(self):
        self.rm.new("TestReference")
        result = self.rm.find_by_name("TestReference")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Reference)

    def test_find_by_name_nonexistent(self):
        self.rm.new("TestReference")
        result = self.rm.find_by_name("NonexistentReference")
        self.assertIsNone(result)

    def test_find_by_attribute(self):
        self.rm.new("TestReference", {"field1": "value1"})
        result = self.rm.find_by_attribute("field1", "value1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "TestReference")

    def test_find_by_attribute_nonexistent(self):
        self.rm.new("TestReference", {"field1": "value1"})
        result = self.rm.find_by_attribute("field2", "value2")
        self.assertEqual(len(result), 0)

    def test_find_by_attribute_partial(self):
        self.rm.new("TestReference", {"field1": "value1"})
        result = self.rm.find_by_attribute("field1", "lue")
        self.assertEqual(len(result), 1)
    
    def test_find_by_attribute_partial_dont_match(self):
        self.rm.new("TestReference", {"field1": "value1"})
        result = self.rm.find_by_attribute("field1", "lue", True)
        self.assertEqual(len(result), 0)
    
    def test_find_by_attribute_exact(self):
        self.rm.new("TestReference", {"field1": "value1"})
        result = self.rm.find_by_attribute("field1", "value1", True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "TestReference")

    def test_remove_reference(self):
        self.rm.new("TestReference")
        result = self.rm.remove("TestReference")
        self.assertTrue(result)
        self.assertEqual(len(self.rm.get_all_references()), 0)

    def test_remove_nonexistent_reference(self):
        result = self.rm.remove("NonexistentReference")
        self.assertFalse(result)

    def test_get_all_references(self):
        self.rm.new("TestReference1")
        self.rm.new("TestReference2")
        result = self.rm.get_all_references()
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], Reference)
        self.assertIsInstance(result[1], Reference)
    
    def test_get_all_fields(self):
        self.rm.new("TestReference1", {"title" : "sample"})
        self.rm.new("TestReference2", {"author" : "test", "title" : "sample"})
        result = self.rm.get_all_fields()
        self.assertEqual(result, ["author", "title"])

    def test_search(self):
        self.rm.new("TestReference1", {"title" : "sample1"})
        self.rm.new("TestReference2", {"author" : "test", "title" : "sample1"})
        self.rm.new("TestReference3", {"title" : "sample2"})
        result = self.rm.search({"title" : "sample"})
        self.assertEqual(len(result), 3)

    def test_search_dont_match(self):
        self.rm.new("TestReference1", {"title" : "sample1"})
        self.rm.new("TestReference2", {"author" : "test", "title" : "sample1"})
        self.rm.new("TestReference3", {"title" : "sample2"})
        result = self.rm.search({"title" : "sample2"}, True)
        self.assertEqual(len(result), 1)

    def test_search_mismatch_case(self):
        self.rm.new("TestReference1", {"title" : "samPLE"})
        result = self.rm.search({"title" : "SAMple"})
        self.assertEqual(len(result), 1)

    def test_search_multiple_terms(self):
        self.rm.new("TestReference1", {"author" : "test1", "title" : "sample1"})
        self.rm.new("TestReference2", {"author" : "test1", "title" : "sample2"})
        self.rm.new("TestReference3", {"author" : "test2", "title" : "sample1"})
        result = self.rm.search({"author" : "test1", "title" : "sample1"})
        self.assertEqual(len(result), 1)