from entry_writer import create_entry
from reference_manager import ReferenceManager
from services.file_manager import read_json_file

manager = ReferenceManager()


while True:
    choice = input(
        "Input 1 to add a new reference\n"
        "Input 2 to list all references\n"
        "Input 3 to load references from a file\n"
        "Input 4 to exit\n").strip()
    if choice == "1":
        entry = create_entry()
        if entry:
            manager.New(entry[0], entry[1])
    elif choice == "2":
        references = manager.GetAllReferences()
        for reference in references:
            print(reference)
    elif choice == "3":
        pass
    elif choice == "4":
        break
    else:
        print("Invalid input")
