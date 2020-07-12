import os
from submission.analysis.conversor_de_dados_adega.utils.situations import PeriodType

def get_all_subjson(path, only_subdir=True, ignore_files=None):
    ignore_files = [] if ignore_files is None else ignore_files

    '''
    Return all json files that is in the subdirectories of a path 
    --
    return: list
    '''
    return_list = []

    if only_subdir:
        subpath = next(os.walk(path))[1]
        for subpath_name in subpath:
            subpath_name = os.path.join(path,subpath_name) 
            for file in os.listdir(subpath_name):
                if file.endswith(".json") and not(file in ignore_files):
                    return_list.append(os.path.join(subpath_name, file))
    else:
        for file in os.listdir(path):
            if file.endswith(".json") and not(file in ignore_files):
                return_list.append(os.path.join(path, file))

    return return_list