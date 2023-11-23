import unittest
from entities.reference import Reference
from reference_manager import ReferenceManager

class TestReferenceManager(unittest.TestCase):
    def setUp(self):
        self.rm = ReferenceManager()

    def test_new_reference(self):
        self.rm.New("TestReference")
        self.assertEqual(len(self.rm.GetAllReferences()), 1)

    def test_add_reference(self):
        reference = Reference("TestReference")
        self.rm.Add(reference)
        self.assertEqual(len(self.rm.GetAllReferences()), 1)

    def test_add_duplicate_reference(self):
        reference1 = Reference("TestReference")
        reference2 = Reference("TestReference")

        self.rm.Add(reference1)

        with self.assertRaises(BaseException):
            self.rm.Add(reference2)

    def test_edit_reference(self):
        self.rm.New("TestReference", {"field1": "value1"})
        result = self.rm.Edit("TestReference", "field1", "new_value")
        self.assertTrue(result)
        self.assertEqual(self.rm.FindByName("TestReference").fields["field1"], "new_value")

    def test_edit_nonexistent_reference(self):
        result = self.rm.Edit("NonexistentReference", "field1", "new_value")
        self.assertFalse(result)

    def test_find_by_name(self):
        self.rm.New("TestReference")
        result = self.rm.FindByName("TestReference")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Reference)

    def test_find_by_name_nonexistent(self):
        result = self.rm.FindByName("NonexistentReference")
        self.assertIsNone(result)

    def test_find_by_attribute(self):
        self.rm.New("TestReference", {"field1": "value1"})
        result = self.rm.FindByAttribute("field1", "value1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "TestReference")

    def test_find_by_attribute_nonexistent(self):
        result = self.rm.FindByAttribute("field1", "value1")
        self.assertEqual(len(result), 0)

    def test_remove_reference(self):
        self.rm.New("TestReference")
        result = self.rm.Remove("TestReference")
        self.assertTrue(result)
        self.assertEqual(len(self.rm.GetAllReferences()), 0)

    def test_remove_nonexistent_reference(self):
        result = self.rm.Remove("NonexistentReference")
        self.assertFalse(result)

    def test_get_all_references(self):
        self.rm.New("TestReference1")
        self.rm.New("TestReference2")
        result = self.rm.GetAllReferences()
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], Reference)
        self.assertIsInstance(result[1], Reference)

if __name__ == '__main__':
    unittest.main()
