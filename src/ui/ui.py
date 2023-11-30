from services.reference_manager import ReferenceManager
from services.entry_writer import create_entry
from services.path import get_full_path
from default_io import DefaultIO


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

    def ask_for_input(self):
        choice = self.io.read(
            "Input a to add a new reference\n"
            "Input l to list all references\n"
            "Input q to exit\n").strip().lower()
        if choice == 'a':
            self.new_entry()
        elif choice == 'l':
            self.io.write(self.list_all_references())
        # elif choice == 'f':
        #     new_file_path = self.io.read("Type new file path here: ").strip()
        #     if not new_file_path:
        #         raise UserInputError("File path must not be empty!")
        #     new_file_name = self.io.read(
        #         "Type new file name here (leave empty for default name): ").strip()
        #     self.change_file_path(new_file_path, new_file_name)
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
