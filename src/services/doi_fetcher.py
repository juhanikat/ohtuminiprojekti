from habanero import Crossref

from resources.bibtex_data import REQUIRED_FIELDS
from services.entry_writer import create_citation_key
from services.validifier import validate_data


def create_entry_by_doi(manager=None):
    """
    Attempts to retrieve data based on user input.

    Returns:
        False, if process is aborted.
        citation_key, fields, if process successfully completed.
    """

    fields = fetch_data()
    if not fields:
        return False

    print("- Retrieved data -")

    for key, value in fields.items():
        print(f"{key}: {value}")

    citation_key = create_citation_key(fields, manager)
    if citation_key is False:
        return False

    print("Reference created using digital object identifier!")
    return citation_key, fields


def fetch_data():
    """
    Prompts an input from the user to fetch an entry based on DOI
    Allocates it inside of dict["entry_type"], if entry_type is valid

    Returns:
        False, if aborting process
        data: dict, if data retrieved successfully
    """

    while True:
        doi = input("Input Digital Identifier of an Object " +
                    "(Enter empty to abort): ").strip()
        if not doi:
            return False

        data = retrieve_data_from_database(doi)

        if not data:
            continue

        data = convert_data(data)

        if data and validate_data(data):
            break

    return data


def retrieve_data_from_database(doi):
    """
    Retrieves data from database using DOI
    Prints errors in case of failure

    Returns:
        False, if a failure
        data : dict, if success
    """
    cr = Crossref()
    try:
        data = cr.works(ids=doi)
        return data['message']
    except Exception as exc:
        print("Error occurred: ", exc)
        return False


def convert_data(data):
    """
    Converts retrieved data from database.

    Returns:
        fields : dict, not validated
    """
    entry_type = data.get('type', '').lower()
    entry_type = convert_entry_type(entry_type)
    entry = {"entry_type": entry_type}

    if entry_type in REQUIRED_FIELDS:
        required_fields = REQUIRED_FIELDS[entry_type]

        for field in required_fields:
            parse_field(field, entry, entry_type, data)

    for key, value in entry.items():
        if value is not None:
            entry[key] = str(value)

    return entry


def convert_entry_type(entry_type):
    if entry_type == "journal-article":
        entry_type = "article"
    return entry_type


def parse_title(data):
    """
    Extracts the title from data, handling both string and list formats.
    """
    title = data.get('title', '')
    return title[0] if isinstance(title, list) and title else title


def parse_year(data):
    """
    Extracts the publication year from data.
    """
    year = data.get('issued', {}).get('date-parts', [[None]])[0][0]
    return year if year is not None else None


def parse_author(data, entry_type):
    """
    Extracts authors, formatted as a string, from data.
    """
    authors = (data.get('editor', []) if entry_type == 'book' and
               'author' not in data else data.get('author', []))
    return ', '.join([f"{a['given']} {a['family']}" for a in authors])


def parse_pages(data):
    """
    Extracts page numbers from data, handling various formats.
    """
    pages = data.get('page', '')
    if pages and '-' in pages:
        first = pages.split('-')[0]
        return first if first.isdigit() else first
    return pages if pages.isdigit() else pages


def parse_field(field, fields, entry_type, data):
    """
    Parses and updates fields from data.
    """
    field_parsers = {
        'title': parse_title,
        'year': parse_year,
        'author': lambda d: parse_author(d, entry_type),
        'pages': parse_pages,
    }

    if field in field_parsers:
        fields[field] = field_parsers[field](data)
    elif field in ['publisher', 'chapter', 'school', 'institution',
                   'note', 'journal', 'booktitle']:
        fields[field] = data.get(field, '')
