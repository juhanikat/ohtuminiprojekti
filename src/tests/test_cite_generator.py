import unittest

import services.cite_generator as generator


class TestCiteGenerator(unittest.TestCase):
    def test_generator_suggests_a_name (self):
        fieldtest = {}
        fieldtest["entry_type"] = "unpublished"
        fieldtest["title"] = "otsikko"
        fieldtest["author"] = "otto"
        fieldtest["note"] = "nootti"

        suggested_name = generator.generate_citation(fieldtest)
        self.assertEqual(suggested_name, "otsikko-otto")

    def test_generator_suggests_a_name_with_different_fields_for_different_entry_type (self):
        fieldtest = {}
        fieldtest["entry_type"] = "book"
        fieldtest["title"] = "otsikko"
        fieldtest["year"] = "2023"

        suggested_name = generator.generate_citation(fieldtest)
        self.assertEqual(suggested_name, "otsikko-2023")

    def test_generator_suggests_less_if_two_fields_not_present (self):
        fieldtest = {}
        fieldtest["entry_type"] = "manual"
        fieldtest["title"] = "otsikko"

        suggested_name = generator.generate_citation(fieldtest)
        self.assertEqual(suggested_name, "otsikko")

    def test_generator_replaces_spaces_with_underscores (self):
        fieldtest = {}
        fieldtest["entry_type"] = "manual"
        fieldtest["title"] = "super otsikko"

        suggested_name = generator.generate_citation(fieldtest)
        self.assertEqual(suggested_name, "super_otsikko")

    def test_generator_does_not_suggest_without_proper_entry_type (self):
        fieldtest = {}
        fieldtest["entry_type"] = "Iamnotaproperentrytype"

        self.assertFalse(generator.generate_citation(fieldtest))

    def test_generator_does_not_suggest_without_required_fields (self):
        fieldtest = {}
        fieldtest["entry_type"] = "misc"

        self.assertFalse(generator.generate_citation(fieldtest))