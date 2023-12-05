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

    folder_path = path.dirname(path.abspath(__file__))

    if not file_name:
        file_name = "data.json"
    if not file_path:
        file_path = "repositories/"
    abs_path = path.join(folder_path, "..", file_path)
    print(abs_path, "\n", folder_path)
    if not path.exists(abs_path):
        makedirs(abs_path)
    full_path = path.join(abs_path, file_name)

    # print(full_path)
    return full_path
