import json
from os import path
from services.reference_manager import ReferenceManager
from services.path import get_full_path


def save_data(references):
    '''
    Saves data to a JSON file.

    This function saves data to a JSON file. It uses the write_json_file
    function to do so.

    Parameters:
    references (ReferenceManager): ReferenceManager object.

    Returns:
    None
    '''

    data = convert_reference_manager_to_dict(references)
    write_json_file(dictionary=data, full_path=references.file_path)


def load_data(full_path=None):
    '''
    Loads data from a JSON file.

    This function loads data from a JSON file. It uses the read_json_file
    function to do so.

    Parameters:
    path (str, optional): Path to the JSON file. Defaults to 
    ./repositories/data.json.

    Returns:
    ReferenceManager: ReferenceManager object.
    '''

    if not full_path or not path.exists(full_path):
        full_path = get_full_path()

    data = read_json_file(full_path=full_path)
    references = convert_dict_to_reference_manager(data)

    return references


def convert_dict_to_reference_manager(data):
    '''
    Converts a dictionary to a ReferenceManager object.

    This function converts a dictionary to a ReferenceManager object. The
    dictionary is formatted as follows:
    {
        <reference name>: {
            "entry_type": "<reference type>",
            "<field name>": "<field value>",
            ...
        },
        ...
    }

    Parameters:
    data (dict): Dictionary that represents the list of Reference objects.

    Returns:
    ReferenceManager: ReferenceManager object.
    '''

    references = ReferenceManager()
    for name, fields in data.items():
        references.new(name, fields)
    return references


def convert_reference_manager_to_dict(references):
    '''
    Converts a ReferenceManager objects to a dictionary.

    This function converts a list of Reference objects to a dictionary. The
    dictionary is formatted as follows:
    {
        <reference name>: {
            "entry_type": "<reference type>",
            "<field name>": "<field value>",
            ...


    Parameters:
    references (ReferenceManager): ReferenceManager object.

    Returns:
    dict: Dictionary that represents the list of Reference objects.
    '''

    data = {}
    for reference in references.get_all_references():
        data[reference.name] = reference.get_fields_as_dict()
    return data


def read_json_file(
        file_path: str = None,
        file_name: str = None,
        full_path: str = None):
    '''
    Reads data from a JSON file, creating a default one if it doesn't exist.

    This function reads a JSON file from file_path/file_name. It defaults to
    "data.json" if file_name is not specified. Similarly, it defaults to
    "/repositories/" for file_path. If the file is missing, it triggers
    write_json_file to create a default file at the specified location.

    Parameters:
    file_path (str, optional): Directory path for the JSON file. Defaults to
    "/repositories/".
    file_name (str, optional): JSON file name. Defaults to "data.json".
    full_path (str, optional): Full path to the JSON file. Defaults to
    file_path/file_name. If specified, file_path and file_name are ignored.

    Returns:
    dict: Data from the JSON file.
    '''
    if not full_path:
        full_path = get_full_path(file_path, file_name)

    if not path.exists(full_path):
        write_json_file(file_path=file_path, file_name=file_name)

    with open(full_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def write_json_file(
        dictionary: dict = None,
        file_path: str = None,
        file_name: str = None,
        full_path: str = None):
    '''
    Writes data to a JSON file. 
    Creates a default file if no dictionary is given.

    This function writes to a JSON file at file_path/file_name. Defaults to
    "data.json" for file_name and "/repositories/" for file_path if not given.
    If no dictionary is provided, an empty one is used.

    Parameters:
    dictionary (dict, optional): Data for the JSON file. Uses empty dictionary 
    if not provided.
    file_path (str, optional): Directory path for the JSON file. Defaults to
    "/repositories/".
    file_name (str, optional): JSON file name. Defaults to "data.json".
    full_path (str, optional): Full path to the JSON file. Defaults to
    file_path/file_name. If specified, file_path and file_name are ignored.

    Returns:
    None
    '''

    if not full_path:
        full_path = get_full_path(file_path, file_name)
    if not dictionary:
        dictionary = {}

    with open(full_path, "w", encoding="utf-8") as file:
        json.dump(dictionary, file, indent=4)
