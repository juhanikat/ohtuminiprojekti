import json
from os import path, makedirs


def read_json_file(file_path: str = None, file_name: str = None):
    '''
    Read data from a JSON file. If the file doesn't exist, it creates a default JSON file.

    The function attempts to read a JSON file located at `file_path`/`file_name`. If `file_name`
    is not provided, it defaults to "data.json". Similarly, if `file_path` is not specified,
    it defaults to "/repositories/". If the specified file does not exist, the function calls 
    `write_json_file` to create a default file at the specified location.

    Parameters:
    file_path (str, optional): The path to the directory containing the JSON file. Defaults to "/repositories/".
    file_name (str, optional): The name of the JSON file. Defaults to "data.json".

    Returns:
    dict: The data read from the JSON file.
    '''

    full_path = get_path(file_path, file_name)

    if not path.exists(full_path):
        write_json_file(file_path=file_path, file_name=file_name)

    with open(full_path, "r") as file:
        data = json.load(file)
    return data


def write_json_file(dictionary: dict = None, file_path: str = None, file_name: str = None):
    '''
    Writes data to a JSON file. If the the dictionary is not provided, it creates a default JSON file.

    The function attempts to write a JSON file located at `file_path`/`file_name`. If `file_name`
    is not provided, it defaults to "data.json". Similarly, if `file_path` is not specified,
    it defaults to "/repositories/".

    Parameters:
    dictionary (dict, optional): The data to be written to the JSON file. Uses empty dictionary if one not provided.
    file_path (str, optional): The path to the directory containing the JSON file. Defaults to "/repositories/".
    file_name (str, optional): The name of the JSON file. Defaults to "data.json".

    Returns:
    None
    '''

    full_path = get_path(file_path, file_name)
    if not dictionary:
        dictionary = {}

    with open(full_path, "w") as file:
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
