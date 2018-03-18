import os

import ujson as json

try:
    from django.conf import settings

    DEBUG = settings.DEBUG
except:
    DEBUG = True


def invert_dict(d):
    return {v: k for k, v in d.items()}


def build_path(path):
    if not os.path.exists(path):
        os.mkdir(path)


def ensure_path_exists(complete_path):
    parts = complete_path.split('/')

    for i in range(len(parts)):
        if not os.path.exists('/'.join(parts[:i+1])):
            os.mkdir('/'.join(parts[:i+1]))


def save_json(path, data):

    ensure_path_exists(os.path.dirname(path))

    params = {} if not DEBUG else {'indent': 4}

    with open(path, 'w') as f:
        json.dump(data, f, **params)


