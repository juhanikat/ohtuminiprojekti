from habanero import Crossref
from services.entry_writer import create_citation_key
from services.validifier import validate_data
from resources.bibtex_data import REQUIRED_FIELDS


def create_entry_by_doi(manager=None):
    """
    Attempts to retrieve data based on user input.

    Returns:
        False, if process is aborted
        citation_key, fields, if process successfully completed
    """

    fields = fetch_data()
    if fields is False:
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

        # for key, value in data.items():
        #    print(f"{key}: {value}")

        if not data:
            continue

        data = convert_data(data)

        if data is not False and validate_data(data):
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
    except Exception as e:
        print("Error occurred: ", e)
        return False


def convert_data(data):
    """
    Converts retrieved data from database.

    Returns:
        fields : dict, not validated
    """
    entry_type = data.get('type', '').lower()
    entry = {"entry_type": entry_type}

    if entry_type in REQUIRED_FIELDS:
        required_fields = REQUIRED_FIELDS[entry_type]

        for field in required_fields:
            parse_field(field, entry, entry_type, data)

    for key in entry:
        if entry[key] is not None:
            entry[key] = str(entry[key])

    return entry


def parse_field(field, fields, entry_type, data):
    """
    Parses fields from data to the entry.
    """
    if field in ['publisher', 'chapter', 'school', 'institution', 'note']:
        fields[field] = data.get(field, '')
    elif field == 'title':
        fields[field] = data.get('title', [''])[0]
    elif field == 'year':
        year = data.get('issued', {}).get('date-parts', [[None]])[0][0]
        fields[field] = year if year is not None else None
    elif field == 'author':
        if entry_type == 'book' and 'author' not in data:
            authors = data.get('editor', [])
        else:
            authors = data.get('author', [])
        fields[field] = ', '.join([f"{author['given']} {author['family']}"
                                  for author in authors])
    elif field in ('journal', 'booktitle'):
        if field in data:
            fields[field] = data[field]
    elif field == 'pages':
        pages = data.get('page', '')
        if pages and '-' in pages:
            first = pages.split('-')[0]
            fields[field] = first if first.isdigit() else first
        else:
            fields[field] = pages if pages.isdigit() else pages
