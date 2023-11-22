from resources.bibtex_data import REQUIRED_FIELDS

def create_entry():
    """
    Creates an entry in dictionary format.

    This function prompts the user to enter required and optional fields.
    The required fields are 'citation' and 'entry_type'.
        Additional required fields may also be included based on the entry type.

    Returns:
        Returns a dictionary if inputs are valid.
        Returns False if the inputs are invalid.
    """

    entry = {}

    # --- Citation key ---

    citation_key = input("Enter the citation key:")
    if citation_key == "":
        return False
    entry["citation"] = citation_key


    # --- Entry type and fields required by it ---

    entry_type = input("Enter the entry type:")
    entry["entry_type"] = entry_type
    if entry_type in REQUIRED_FIELDS:
        for field in REQUIRED_FIELDS[entry_type]:
            value = input(f"Enter value for {field}: ")
            if value == "":
                print ("Value must be included for a required field!")
                return False
            entry[field] = value
    else:
        print ("Invalid entry type!")
        return False


    # --- Optional fields ---

    while True:
        field = input("Enter field name (leave empty to finish):").strip()
        if not field:
            break

        if field in entry:
            print(f"The field '{field}' has already been entered. Please enter a different field.")
            continue

        value = input(f"Enter value for {field}:")
        entry[field] = value

    return entry
