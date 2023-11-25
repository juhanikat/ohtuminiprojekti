from resources.bibtex_data import REQUIRED_FIELDS
from services.validifier import validate_input

def create_entry(manager = None):
    """
    Creates an entry in a string, dictionary format.

    This function prompts the user to enter required and optional fields.
    The required fields are 'citation' and 'entry_type'.
        Additional required fields may also be included based on the entry type.

    Parameters:
        Reference Manager, if the manager exists, check for duplicate entries based on input

    Returns:
        string, dictionary: name, fields if the inputs are valid.
        bool: False if the inputs are invalid, or if citation key is a duplicate.
    """

    fields = {}

    citation_key = create_citation_key(manager)
    if citation_key is False:
        return False

    if choose_entry_type(fields) == False:
        return False
    
    if fill_required_fields(fields) == False:
        return False

    enter_optional_fields(fields)

    return citation_key, fields

def create_citation_key(manager):
    """
    Creates a citation key and returns it based on input if valid.

    Params:
        Reference Manager, if the manager exists, check for duplicate entries based on input

    Returns:
        citation_key as input, if input is valid
        False if the inputs are invalid.
    """

    citation_key = input("Enter the citation key:").strip()
    if not validate_input("citation",citation_key):
        return False

    if manager != None and manager.FindByName(citation_key):
        print("Citation already exists!")
        return False
    
    return citation_key

def choose_entry_type(fields):
    """
    Chooses an entry type based on input and allocates it inside of dict["entry_type"], if entry_type is valid

    Returns:
        False, if inputs invalid
    """
    entry_types = ", ".join(REQUIRED_FIELDS.keys())
    print(f"Possible entry types: {entry_types}")

    entry_type = input("Choose the entry type:").strip()
    if not validate_input("entry_type", entry_type):
        return False

    fields["entry_type"] = entry_type

def fill_required_fields(fields):
    """
    Prompts the required fields based on entry_type and fills the information inside the dict[fields] if inputs are valid

    Returns:
        False, if inputs invalid
    """
    for field in REQUIRED_FIELDS[fields["entry_type"]]:
        value = input(f"Enter value for {field}: ").strip()
        if not validate_input(field, value):
            return False
        fields[field] = value

def enter_optional_fields(fields):
    """
    Prompts for optional fields based on user input, populating the information into dict[fields] if inputs are valid.
    """
    while True:
        field = input("Enter optional field name (leave empty to finish):").strip()
        if not field:
            break

        if field in fields or field == "citation":
            print(f"The field '{field}' has already been entered. Enter a different field.")
            continue

        value = input(f"Enter value for {field}:").strip()

        if not validate_input(field, value):
            continue

        fields[field] = value