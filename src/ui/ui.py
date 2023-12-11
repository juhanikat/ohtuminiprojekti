from terminaltables import AsciiTable

from resources.bibtex_data import REQUIRED_FIELDS
from services.bibtex_export import export_to_bibtex
from services.doi_fetcher import create_entry_by_doi
from services.entry_writer import create_entry
from services.path import get_full_path
from services.reference_manager import ReferenceManager


class UserInputError(Exception):
    """Raised when the user inputs something incorrect"""
    pass


class UI:
    def __init__(self, manager: ReferenceManager):
        self.manager = manager

    def create_type_table(self, type: str, references: list) -> str:
        """
        Creates an AsciiTable containing all inputted references of a specific type.

        Args:
            type: The type of reference, for example 'article', 'book' etc.
            references: List of references.

        Returns:
            The table as a string.
        """
        required_fields = REQUIRED_FIELDS[type]
        max_cell_length = 30
        max_extra_fields = 3

        table = []
        heading = ["name"] + required_fields + ["extra fields"]
        table.append(heading)
        for reference in references:
            # limits cell content to length specified in max_cell_length
            new_row = [reference.name[:max_cell_length - 3] + "..."
                       if len(reference.name) > max_cell_length else reference.name]

            fields = reference.get_fields_as_dict()
            for field in required_fields:
                cell_content = str(fields[field])
                # limits cell content to length specified in max_cell_length
                if len(cell_content) > max_cell_length:
                    cell_content = cell_content[:max_cell_length - 3] + "..."
                new_row.append(cell_content)

            extra_fields = [
                key for key in fields if key not in required_fields and key != "entry_type"]
            # limits the amount of extra fields to number specified in max_extra_fields
            if len(extra_fields) > max_extra_fields:
                extra_fields = extra_fields[:max_extra_fields]
                extra_fields.append("...")

            new_row.append(", ".join(extra_fields))
            # adds new_row to the table
            table.append(new_row)

        table = AsciiTable(table, type)
        return "\n" + table.table

    def create_all_tables(self, references: list = []):
        """
        Uses create_type_table() to create a table for every type of reference. Doesn't create a table if no references of that type exist.

        Args:
            references (optional): Use these references instead of the ones in the reference manager.

        Returns:
            The table as a string.
        """
        big_table = ""
        for type in REQUIRED_FIELDS:
            if not references:
                references_of_type = self.manager.find_by_attribute(
                    "entry_type", type)
            else:
                references_of_type = [
                    ref for ref in references if ref.get_type() == type]
            if not references_of_type:
                continue
            subtable = self.create_type_table(type, references_of_type)
            if subtable:
                big_table += subtable + "\n"

        return big_table

    def new_entry(self):
        entry = create_entry(self.manager)
        if entry:
            # creates new Reference object and adds it to the manager
            self.manager.new(entry[0], entry[1])
        return entry

    def new_entry_using_doi(self):
        entry = create_entry_by_doi(self.manager)
        if entry:
            # creates new Reference object using doi and adds it to the manager
            self.manager.new(entry[0], entry[1])
        return entry

    def manager_search(self):
        possible_fields = self.manager.get_all_fields()
        print(f"Possible fields: {', '.join(possible_fields)}\n")

        search_dict = {}

        while True:
            if search_dict:
                # prints out what you are currently searching for
                current_search = [
                    key + ':' + value for (key, value) in search_dict.items()]
                print(f"Currently searching for: {', '.join(current_search)}")

            field = input(
                "Enter a field to search in (leave empty to start search): ").strip()
            if field == "":
                break
            if field not in possible_fields:
                print(f"No references with a value for '{field}'")
                continue

            value = input(f"Enter value for '{field}': ").strip()
            if not value:
                print("Value must not be empty!")
                continue

            search_dict[field] = value
            print("")

        return self.manager.search(search_dict)

    def ask_for_input(self):
        choice = input(
            "Input a to add a new reference\n"
            "Input g to get a new reference using DOI\n"
            "Input l to list all references\n"
            "Input r to remove a reference\n"
            "Input e to export references as a .bib file\n"
            "Input s to search references\n"
            "Input q to exit and save references to file\n").strip().lower()

        if choice == 'a':
            self.new_entry()

        elif choice == 'g':
            self.new_entry_using_doi()

        elif choice == 'l':
            # prints all saved references as a table
            print(self.create_all_tables())

        elif choice == 'e':
            export_to_bibtex(self.manager)
            print("Exported!")

        elif choice == 'r':
            remove_key = input(
                "Type the name of the reference to remove: ").strip()
            if not remove_key:
                raise UserInputError("Name must not be empty!")
            success = self.manager.remove(remove_key)
            if success:
                print(f"Removed reference with name: {remove_key}")
            else:
                print(f"Reference with name '{remove_key}' not found")

        elif choice == 's':
            found_references = self.manager_search()
            if not found_references:
                print("No references found")
            print(self.create_all_tables(found_references))

        elif choice == 'q':
            return -1

        else:
            raise UserInputError("Invalid input")

    def ui_loop(self):
        while True:
            result = None
            try:
                result = self.ask_for_input()
            except UserInputError as error:
                print(str(error) + "\n")
                continue
            if result == -1:
                return -1
            print("")
