from services.cite_generator import generate_citation
from services.validifier import validate_input
from resources.bibtex_data import REQUIRED_FIELDS


def create_entry(manager=None):
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

    fields = {}

    if choose_entry_type(fields) is False:
        return False

    if fill_required_fields(fields) is False:
        return False

    enter_optional_fields(fields)

    citation_key = create_citation_key(fields, manager)
    if citation_key is False:
        return False

    return citation_key, fields


def create_citation_key(fields, manager):
    """
    Creates a citation key and returns it based on input if valid.

    Params:
        Reference Manager, check for duplicate entries based on input

    Returns:
        citation_key as input, if input is valid
        False if the inputs are invalid.
    """

    while True:
        suggested_citation = generate_citation(fields, manager)
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

        if manager is not None and manager.find_by_name(citation_key):
            print("Citation already exists!")
            continue

        return citation_key


def choose_entry_type(fields):
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
            fields["entry_type"] = entry_type
            break

    return fields


def fill_required_fields(fields):
    """
    Prompts the required fields based on entry_type.
    Fills the information inside the dict[fields] if inputs are valid

    Returns:
        False, if user sends empty input
    """

    while True:
        result = _enter_required_fields(fields)
        if result == "Abort":
            return False
        if result:
            break

    return fields


def _enter_required_fields(fields):
    """
    Prompts the required fields based on entry_type.
    Fills the information inside the dict[fields] if inputs are valid

    Returns:
        False, if validation fails
        True, if all required fields are valid
        Abort, if user enters an empty field.
    """
    for field in REQUIRED_FIELDS[fields["entry_type"]]:
        if field in fields:
            continue

        value = input(f"Enter value for {field} " +
                      "(Enter empty to abort): ").strip()

        if not value:
            return "Abort"

        if not validate_input(field, value):
            return False
        fields[field] = value
    return True


def enter_optional_fields(fields):
    """
    Prompts for optional fields based on user input.
    Populates the information into dict[fields] if inputs are valid.
    """
    while True:
        field = input("Enter optional field name " +
                      "(Leave empty to finish):").strip()
        if not field:
            break

        if field in fields or field == "citation":
            print(f"The field '{field}' has already been entered. " +
                  "Enter a different field.")
            continue

        value = input(f"Enter value for {field}:").strip()

        if not validate_input(field, value):
            continue

        fields[field] = value
