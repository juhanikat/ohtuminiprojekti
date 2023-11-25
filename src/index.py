from services.entry_writer import create_entry
from services.reference_manager import ReferenceManager


def list_all_references(manager) -> str:
    references = manager.GetAllReferences()
    result = ""
    for reference in references:
        result += reference.__str__() + "\n"
    return result


def new_entry(manager):
    entry = create_entry(manager)
    if entry:
        # creates new Reference object and adds it to the manager
        manager.New(entry[0], entry[1])
    return entry


def main():
    manager = ReferenceManager()
    while True:
        choice = input(
            "Input a to add a new reference\n"
            "Input l to list all references\n"
            "Input q to exit\n").strip().lower()
        if choice == 'a':
            new_entry(manager)
        elif choice == 'l':
            print(list_all_references(manager))
        elif choice == 'q':
            break
        else:
            print("Invalid input")
        print()


if __name__ == "__main__":
    main()
