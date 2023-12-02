from resources.bibtex_data import REQUIRED_FIELDS

def generate_citation (fields, manager = None):
    """
    Generates a citation string as a suggestion.
    Takes in fields and manager as parameters, which
        will be used to generate the string.

    Parameters:
        Fields: Dictionary. Suggestions are based on info available here.
        Manager: Reference_Manager. To check for duplicates.

    Returns:
        False, if a suggestion failed to generate
        Value, if a suggestion was generated
    """

    entry = fields["entry_type"]
    if entry not in REQUIRED_FIELDS:
        return False

    required_fields = REQUIRED_FIELDS[entry][:2]
    suggestion_parts = [fields.get(field, "") for field in required_fields]
    suggestion = "-".join(suggestion_parts)
    suggestion = suggestion.replace(" ","_")

    if not suggestion:
        return False

    if manager is not None and manager.find_by_name(suggestion):
        return False

    return f"{entry}-"+suggestion
