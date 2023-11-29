from os import path, makedirs


def get_full_path(file_path: str = None, file_name: str = None):
    '''
    Returns full path to file.

    This function returns the full path to a file. It defaults to
    "data.json" for file_name and "/repositories/" for file_path 
    if not given. If the directory doesn't exist, it creates it.


    Parameters:
    file_path (str, optional): Directory path for the JSON file. Defaults to
    "/repositories/".
    file_name (str, optional): JSON file name. Defaults to "data.json".
    '''
    if not file_name:
        file_name = "data.json"
    if not file_path:
        file_path = "./repositories/"
    if not path.exists(file_path):
        makedirs(file_path)

    full_path = path.join(file_path, file_name)
    return full_path
