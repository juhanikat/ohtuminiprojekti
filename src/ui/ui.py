from services.reference_manager import ReferenceManager
from services.entry_writer import create_entry
from services.path import get_full_path


class UserInputError(Exception):
    pass


def change_file_path(manager: ReferenceManager, new_file_path: str, new_file_name: str = None):
    '''
    Changes the file_path variable of the reference manager.

    Parameters:
    manager: A ReferenceManager object.
    new_file_path: The path of the new file location.
    new_file_name: The new file name.

    Returns:
    None


    '''
    manager.file_path = get_full_path(new_file_path, new_file_name)


def list_all_references(manager: ReferenceManager) -> str:
    references = manager.get_all_references()
    result = ""
    for reference in references:
        result += reference.__str__() + "\n"
    return result


def new_entry(manager: ReferenceManager):
    entry = create_entry(manager)
    if entry:
        # creates new Reference object and adds it to the manager
        manager.new(entry[0], entry[1])
    return entry


def ask_for_input(manager: ReferenceManager):
    choice = input(
        "Input a to add a new reference\n"
        "Input l to list all references\n"
        "Input f to change the save file location\n"
        "Input q to exit\n").strip().lower()
    if choice == 'a':
        new_entry(manager)
    elif choice == 'l':
        print(list_all_references(manager))
    elif choice == 'f':
        new_file_path = input("Type new file path here: ").strip()
        if not new_file_path:
            raise UserInputError("File path must not be empty!")
        new_file_name = input(
            "Type new file name here (leave empty for default name): ").strip()
        change_file_path(manager, new_file_path, new_file_name)
    elif choice == 'q':
        return -1
    else:
        print("Invalid input")
    print()


def ui_loop(manager: ReferenceManager):
    while True:
        result = None
        try:
            result = ask_for_input(manager)
        except UserInputError as error:
            print(error)
            continue
        if result == -1:
            break
