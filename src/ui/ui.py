from services.reference_manager import ReferenceManager
from services.entry_writer import create_entry
from services.path import get_full_path
from default_io import DefaultIO
from bibtex_export import export_to_bibtex
from terminaltables import AsciiTable
from resources.bibtex_data import REQUIRED_FIELDS


class UserInputError(Exception):
    pass


class UI:
    def __init__(self, manager: ReferenceManager, io=DefaultIO()):
        self.manager = manager
        self.io = io

    def change_file_path(self, new_file_path: str, new_file_name: str = None):
        '''
        Changes the file_path variable of the reference manager.

        Parameters:
        manager: A ReferenceManager object.
        new_file_path: The path of the new file location.
        new_file_name: The new file name.

        Returns:
        None


        '''
        self.manager.file_path = get_full_path(new_file_path, new_file_name)

    def create_type_table(self, type, references):
        """
        Creates an AsciiTable containing all inputted references of a specific type.

        Args:
            type: The type of reference, for example 'article', 'book' etc.
            references: List of references.

        Returns:
            The table as a string.
        """
        required_fields = REQUIRED_FIELDS[type]

        table = []
        heading = ["name", "type"] + required_fields
        table.append(heading)
        for reference in references:
            new_row = [reference.name, reference.get_type()]
            fields = reference.get_fields_as_dict()
            for field in required_fields:
                new_row.append(fields[field])
            table.append(new_row)

        table = AsciiTable(table, type)
        return table.table

    def create_all_tables(self, references=None):
        """
        Uses create_type_table() to create a table for every type of reference. Doesn't create a table if no references of that type exist.

        Args:
            references (optional): Use these references instead of the ones in the reference manager.

        Returns:
            The table as a string.
        """
        big_table = ""
        for type in REQUIRED_FIELDS:
            if references is None:
                references_of_type = self.manager.find_by_attribute(
                    "entry_type", type)
            else:
                references_of_type = [
                    ref for ref in filter(
                        lambda ref: ref.get_type() == type,
                        references)]
            if not references_of_type:
                continue
            subtable = self.create_type_table(type, references_of_type)
            if subtable:
                big_table += subtable + "\n"

        return big_table

    def list_all_references(self) -> str:
        references = self.manager.get_all_references()
        result = ""
        for reference in references:
            result += reference.__str__() + "\n"
        return result

    def new_entry(self):
        entry = create_entry(self.manager)
        if entry:
            # creates new Reference object and adds it to the manager
            self.manager.new(entry[0], entry[1])
        return entry

    def manager_search(self):
        possible_fields = self.manager.get_all_fields()
        self.io.write(f"Possible fields: {possible_fields}\n")

        search_dict = {}

        while True:
            field = self.io.read(
                "Enter a field to search in (leave empty to start search): ")
            if field == "":
                break
            if field not in possible_fields:
                self.io.write(f"No references with a value for '{field}'")
                continue
            value = self.io.read(f"Enter value for '{field}': ")
            search_dict[field] = value

        return self.manager.search(search_dict)

    def ask_for_input(self):
        choice = self.io.read(
            "Input a to add a new reference\n"
            "Input l to list all references\n"
            "Input r to remove a reference\n"
            "Input e to export references as a .bib file\n"
            "Input s to search references\n"
            "Input q to exit\n").strip().lower()
        if choice == 'a':
            self.new_entry()
        elif choice == 'l':
            # prints all saved references as a table
            self.io.write(self.create_all_tables())
        elif choice == 'f':
            new_file_path = self.io.read("Type new file path here: ").strip()
            if not new_file_path:
                raise UserInputError("File path must not be empty!")
            new_file_name = self.io.read(
                "Type new file name here (leave empty for default name): ").strip()
            self.change_file_path(new_file_path, new_file_name)
        elif choice == 'e':
            export_to_bibtex(self.manager)
        elif choice == 'r':
            remove_key = self.io.read(
                "Type the name of the reference to remove: ").strip()
            success = self.manager.remove(remove_key)
            if success:
                self.io.write(f"Removed reference with name: {remove_key}")
            else:
                self.io.write(f"Reference with name '{remove_key}' not found")
        elif choice == 's':
            found_references = self.manager_search()
            self.io.write(self.create_all_tables(found_references))
        elif choice == 'q':
            return -1
        else:
            self.io.write("Invalid input")
        self.io.write("")

    def ui_loop(self):
        while True:
            result = None
            try:
                result = self.ask_for_input()
            except UserInputError as error:
                self.io.write(error)
                continue
            if result == -1:
                return -1
