import json
from os import path, makedirs


def read_json_file(file_path: str = None, file_name: str = None):
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

    Returns:
    dict: Data from the JSON file.
    '''

    full_path = get_path(file_path, file_name)

    if not path.exists(full_path):
        write_json_file(file_path=file_path, file_name=file_name)

    with open(full_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def write_json_file(
        dictionary: dict = None,
        file_path: str = None,
        file_name: str = None):
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

    Returns:
    None
    '''
    full_path = get_path(file_path, file_name)
    if not dictionary:
        dictionary = {}

    with open(full_path, "w", encoding="utf-8") as file:
        json.dump(dictionary, file)


def get_path(file_path: str = None, file_name: str = None):
    if not file_name:
        file_name = "data.json"
    if not file_path:
        file_path = "./repositories/"
    if not path.exists(file_path):
        makedirs(file_path)

    full_path = path.join(file_path, file_name)
    return full_path
