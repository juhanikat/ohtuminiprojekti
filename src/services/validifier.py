from resources.bibtex_data import REQUIRED_FIELDS

def validate_input(type, value):
    """
    Validates the input based on the type and value set as parameters.
    Use only if you have a type that exists in FIELD_VALIDATORS. Otherwise use the other functions available!

    Returns:
        True, if the value is valid or if type is not found within the FIELD_VALIDATORS
        False, if the value is invalid
    """

    if type in FIELD_VALIDATORS:
        validators = FIELD_VALIDATORS[type]
        if isinstance(validators, list):
            for validator in validators:
                if not validator(value):
                    return False
        else:
            if not validators(value):
                return False
        return True
    else:
        return True # Default behaviour when no type is found


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
        else:
            print ("Value must be a positive number!")
            return False
    except ValueError:
        print ("Value was not a number!")
        return False


def validate_no_whitespace(value):
    """
    Validates whether input is a string and does not contain whitespace before or after the string

    Returns:
        True, if the value string and no whitespace present
        False, if the value string and whitespace present
    """
    if isinstance(value, str) and not value.strip() == value:
        print ("Value contains whitespace!")
        return False
    else:
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
    else:
        print ("Value can not be empty!")
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
    
    print ("Invalid entry type!")
    return False


FIELD_VALIDATORS = {
    "year": validate_as_positive_integer,
    "citation": [validate_no_whitespace, validate_no_empty],
    "entry_type": validate_has_an_entry_type,
    "author": [validate_no_whitespace, validate_no_empty],
    "title": [validate_no_whitespace, validate_no_empty],
    "journal": [validate_no_whitespace, validate_no_empty],
    "publisher": [validate_no_whitespace, validate_no_empty],
    "booktitle": [validate_no_whitespace, validate_no_empty],
    "chapter": [validate_no_whitespace, validate_no_empty],
    "pages": validate_as_positive_integer,
    "school": [validate_no_whitespace, validate_no_empty],
    "note": [validate_no_whitespace, validate_no_empty],
}