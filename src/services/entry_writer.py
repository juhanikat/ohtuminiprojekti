from services.cite_generator import generate_citation
from services.validifier import validate_input
from resources.bibtex_data import REQUIRED_FIELDS
from services.reference_manager import ReferenceManager
from default_io import DefaultIO


class EntryWriter:

    def __init__(self, manager: ReferenceManager, io=DefaultIO()):
        self.manager = manager
        self.io = io
        self.fields = {}

    def create_entry(self):
        """
        Creates an entry in a string, dictionary format.

        This function prompts the user to enter required and optional fields.
        The required fields are 'citation' and 'entry_type'.
            Additional required fields may also be included based on the entry type.

        Parameters:
            Reference Manager, check for duplicate entries based on input

        Returns:
            string, dictionary: name, fields if the inputs are valid.
            bool: False if the inputs are invalid.
        """

        if self.choose_entry_type() is False:
            return False

        if self.fill_required_fields() is False:
            return False

        self.enter_optional_fields()

        citation_key = self.create_citation_key()
        if citation_key is False:
            return False

        return citation_key, self.fields

    def create_citation_key(self):
        """
        Creates a citation key and returns it based on input if valid.

        Params:
            Reference Manager, check for duplicate entries based on input

        Returns:
            citation_key as input, if input is valid
            False if the inputs are invalid.
        """

        while True:
            suggested_citation = generate_citation(self.fields, self.manager)
            if suggested_citation is not False:
                print("Recommended name for citation: " + suggested_citation +
                      " input 'x' to use it automatically.")

            citation_key = input("Enter the citation key " +
                                 "(Enter empty to abort): ").strip()

            if suggested_citation is not False and citation_key == 'x':
                citation_key = suggested_citation

            if not citation_key:
                return False

            if not validate_input("citation", citation_key):
                continue

            if self.manager is not None and self.manager.find_by_name(citation_key):
                print("Citation already exists!")
                continue

            return citation_key

    def choose_entry_type(self):
        """
        Chooses an entry type based on input
        Allocates it inside of dict["entry_type"], if entry_type is valid

        Returns:
            False, if inputs invalid
        """

        entry_types = ", ".join(REQUIRED_FIELDS.keys())
        print(f"Possible entry types: {entry_types}")

        while True:
            entry_type = input("Choose the entry type " +
                               "(Enter empty to abort): ").strip()
            if not entry_type:
                return False

            if validate_input("entry_type", entry_type):
                self.fields["entry_type"] = entry_type
                break

        return self.fields

    def fill_required_fields(self):
        """
        Prompts the required self.fields based on entry_type.
        Fills the information inside the dict[self.fields] if inputs are valid

        Returns:
            False, if user sends empty input
        """

        while True:
            result = self._enter_required_fields()
            if result == "Abort":
                return False
            if result:
                break

        return self.fields

    def _enter_required_fields(self):
        """
        Prompts the required self.fields based on entry_type.
        Fills the information inside the dict[self.fields] if inputs are valid

        Returns:
            False, if validation fails
            True, if all required self.fields are valid
            Abort, if user enters an empty field.
        """
        for field in REQUIRED_FIELDS[self.fields["entry_type"]]:
            if field in self.fields:
                continue

            value = input(f"Enter value for {field} " +
                          "(Enter empty to abort): ").strip()

            if not value:
                return "Abort"

            if not validate_input(field, value):
                return False
            self.fields[field] = value
        return True

    def enter_optional_fields(self):
        """
        Prompts for optional fields based on user input.
        Populates the information into dict[self.fields] if inputs are valid.
        """
        while True:
            field = input("Enter optional field name " +
                          "(Leave empty to finish):").strip()
            if not field:
                break

            if field in self.fields or field == "citation":
                print(f"The field '{field}' has already been entered. " +
                      "Enter a different field.")
                continue

            value = input(f"Enter value for {field}:").strip()

            if not validate_input(field, value):
                continue

            self.fields[field] = value
