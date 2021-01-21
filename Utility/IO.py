from shutil import rmtree
from os.path import isdir
from os import mkdir

def clear_directory(directory_name):
    if not isdir(directory_name):
        mkdir(directory_name)
    else:
        rmtree(directory_name)
        mkdir(directory_name)