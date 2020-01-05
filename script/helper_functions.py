from os import listdir


def get_key():
    """Get key based on file names in meta_data folder"""
    files_list = listdir(r'C:\Users\areeb\Documents\Programming\Pycharm Projects\django_pied_piper\media\metadata')

    for i in range(0, 255):
        name = f'{i}.dat'

        if not files_list.__contains__(name):
            return i
