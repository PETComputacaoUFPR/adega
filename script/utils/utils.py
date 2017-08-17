import os

def build_path(path):
    if not os.path.exists(path):
        os.mkdir(path)
