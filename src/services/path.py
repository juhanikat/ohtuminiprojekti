import os


def get_full_path(file_path="repositories",
                  file_name="data.json",
                  full_path=None):
    '''
    Returns full path to file.

    This function returns the full path to a file. It defaults to
    "data.json" for file_name and "repositories" for file_path 
    if not given. If the directory doesn't exist, it creates it.

    Parameters:
    file_path (str, optional): Directory path for the JSON file. Defaults to
    "repositories".
    file_name (str, optional): JSON file name. Defaults to "data.json".
    '''

    folder_path = os.path.dirname(os.path.abspath(__file__))

    if full_path:
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        return os.path.join(folder_path, "..", full_path)

    abs_path = os.path.join(folder_path, "..", file_path)
    if not os.path.exists(abs_path):
        os.makedirs(abs_path)

    return os.path.join(abs_path, file_name)
