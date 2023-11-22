def create_entry():
    """
    Creates an entry in dictionary format.

    This function prompts the user to enter required and optional fields.
    The required fields are 'citation' and 'entry_type'

    Returns:
        Returns a dictionary if inputs are valid.
        Returns False if the inputs are invalid.
    """

    entry = {}

    citation_key = input("Enter the citation key:")
    entry["citation"] = citation_key

    entry_type = input("Enter the entry type:")
    entry["entry_type"] = entry_type

    while True:
        field = input("Enter field name (leave empty to finish):").strip()
        if not field:
            break

        value = input(f"Enter value for {field}:")
        entry[field] = value

    if entry["citation"] == "":
        return False

    if entry["entry_type"] == "":
        return False

    return entry
