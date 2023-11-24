import unittest
import services.validifier as validifier

class TestValidifier(unittest.TestCase):
    def test_validate_as_positive_integer_positive_integer_returns_true (self):
        self.assertTrue(validifier.validate_as_positive_integer(5))
        
    def test_validate_as_positive_integer_negative_integer_returns_false (self):
        self.assertFalse(validifier.validate_as_positive_integer(-5))

    def test_validate_as_positive_integer_text_returns_false (self):
        self.assertFalse(validifier.validate_as_positive_integer("Iamnotanumber"))

    def test_validate_no_white_space_with_text_returns_true (self):
        self.assertTrue(validifier.validate_no_whitespace("no whitespace"))

    def test_validate_no_white_space_with_text_returns_false_when_whitespace_present (self):
        self.assertFalse(validifier.validate_no_whitespace("  no whitespace"))
        self.assertFalse(validifier.validate_no_whitespace("no whitespace  "))

    def test_validate_as_no_empty_text_returns_true (self):
        self.assertTrue(validifier.validate_no_empty("Iamnotempty"))

    def test_validate_as_no_empty_empty_text_returns_false (self):
        self.assertFalse(validifier.validate_no_empty(""))

    def test_validate_has_an_entry_type_with_valid_type (self):
        self.assertTrue(validifier.validate_has_an_entry_type("book"))

    def test_validate_has_no_entry_type_with_invalid_type (self):
        self.assertFalse(validifier.validate_has_an_entry_type("Idontexist"))

