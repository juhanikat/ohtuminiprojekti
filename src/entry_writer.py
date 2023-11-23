from resources.bibtex_data import REQUIRED_FIELDS

def create_entry():
    """
    Creates an entry in dictionary format.

    This function prompts the user to enter required and optional fields.
    The required fields are 'citation' and 'entry_type'.
        Additional required fields may also be included based on the entry type.

    Returns:
        string, dictionary: name, fields if the inputs are valid.
        bool: False if the inputs are invalid.
    """

    fields = {}

    # --- Citation key ---

    citation_key = input("Enter the citation key:")
    if citation_key == "":
        print ("Value must not be empty!")
        return False


    # --- Entry type and fields required by it ---

    entry_type = input("Enter the entry type:")
    fields["entry_type"] = entry_type
    if entry_type in REQUIRED_FIELDS:
        for field in REQUIRED_FIELDS[entry_type]:
            value = input(f"Enter value for {field}: ")
            if value == "":
                print ("Value must be included for a required field!")
                return False
            fields[field] = value
    else:
        print ("Invalid entry type!")
        return False


    # --- Optional fields ---

    while True:
        field = input("Enter optional field name (leave empty to finish):").strip()
        if not field:
            break

        if field in fields or field == "citation":
            print(f"The field '{field}' has already been entered. Enter a different field.")
            continue

        value = input(f"Enter value for {field}:")

        if value == "":
            print("Value must not be empty! Enter a different value.")
            continue

        fields[field] = value

    return citation_key, fields