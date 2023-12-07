import os


def get_all_file_paths(target_directory):
    try:
        files = [f for f in os.listdir(target_directory)]
        return files
    except FileNotFoundError:
        raise


def get_file_path(filename, target_directory):
    try:
        files = get_all_file_paths(target_directory)
        if filename in files:
            return os.path.join(target_directory, filename)
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise
