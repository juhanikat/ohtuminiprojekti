from resources.bibtex_data import REQUIRED_FIELDS


def validate_input(field_type, value):
    """
    Validates the input based on the type and value set as parameters.
    Use only if you have a type that exists in FIELD_VALIDATORS.
    Otherwise use the other functions available!

    Returns:
        True, if the value is valid, or if type not found
        False, if the value is invalid
    """

    if field_type not in FIELD_VALIDATORS:
        return True  # Default behaviour when no type is found

    validators = FIELD_VALIDATORS[field_type]

    if isinstance(validators, list):
        if any(not validator(value) for validator in validators):
            return False
    else:
        if not validators(value):
            return False

    return True


def validate_data (data):
    """
    Validifies all fields in data

    Parameters:
        data, dict.

    Returns:
        False, if aborting process
        data: dict, if data retrieved successfully
    """
    entry_type = data.get('entry_type', '').lower()

    required_fields = REQUIRED_FIELDS.get(entry_type, [])
    for field in required_fields:
        if field not in data:
            print(f"Missing required field: {field}")
            return False
        if not validate_input(field, data[field]):
            print(f"Invalid data for field: {field}")
            return False

    for key, value in data.items():
        if not validate_input(key, value):
            print("Invalid data!")
            return False

    return True


def validate_as_positive_integer(value):
    """
    Validates whether input is a positive number

    Returns:
        True, if the value is a positive integer
        False, if the value is not a positive integer
    """
    try:
        integer = int(value)
        if integer > 0:
            return True

        print("Value must be a positive number!")
        return False
    except ValueError:
        print("Value was not a number!")
        return False


def validate_no_whitespace(value):
    """
    Validates whether input is a string and does not contain whitespace

    Returns:
        True, if the value string and no whitespace present
        False, if the value string and whitespace present
    """
    if isinstance(value, str) and not value.strip() == value:
        print("Value contains whitespace!")
        return False

    return True


def validate_no_empty(value):
    """
    Validates whether input is a string and does not contain any text

    Returns:
        True, if the value string and not empty
        False, if the value string and empty
    """
    if isinstance(value, str) and len(value.strip()) > 0:
        return True

    print("Value can not be empty!")
    return False

def validate_no_spaces(value):
    """
    Validates whether input is a string and contains any spaces

    Returns:
        True, if the value does not contain spaces anywhere
        False, if the value contains spaces
    """
    if isinstance(value, str) and value.count(' ') == 0:
        return True

    print("Value can not contain spaces!")
    return False


def validate_has_an_entry_type(value):
    """
    Validates whether input is matches a valid entry type in REQUIRED_FIELDS

    Returns:
        True, if the matching value exists
        False, if the matching value does not exist
    """
    if value in REQUIRED_FIELDS:
        return True

    print("Invalid entry type!")
    return False


FIELD_VALIDATORS = {
    "year": validate_as_positive_integer,
    "citation": [validate_no_whitespace, validate_no_empty, validate_no_spaces],
    "entry_type": validate_has_an_entry_type,
    "author": [validate_no_whitespace, validate_no_empty],
    "title": [validate_no_whitespace, validate_no_empty],
    "journal": [validate_no_whitespace, validate_no_empty],
    "publisher": [validate_no_whitespace, validate_no_empty],
    "booktitle": [validate_no_whitespace, validate_no_empty],
    "chapter": [validate_no_whitespace, validate_no_empty],
    "pages": [validate_no_whitespace, validate_no_empty],
    "school": [validate_no_whitespace, validate_no_empty],
    "note": [validate_no_whitespace, validate_no_empty],
}
