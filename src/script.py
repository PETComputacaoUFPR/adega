# -*- coding: utf-8 -*-
import sys
import os
import django
import time
import json
import io
import math

from datetime import timedelta
from pathlib import Path

sys.path.append(os.getcwd())
os.environ["DJANGO_SETTINGS_MODULE"] = "adega.settings"
django.setup()

from django.db import models
from student.models import *
from course.models import *
from degree.models import *
from admission.models import *

from student.analysis import *
from course.analysis import *
from degree.analysis import *
from admission.analysis import *
from utils.data import *
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

def main():
    start_time = time.clock()
    start_time_exec = time.time()

    generate_data()

    print("--- Tempo de cpu: {} ---".format(timedelta(seconds=round(time.clock() - start_time))))
    print("--- Duração real: {} ---".format(timedelta(seconds=round(time.time() - start_time_exec))))


def generate_data():
    path = 'cache'
    if not os.path.exists(path):
        os.mkdir(path)

    path = 'cache/curso'
    if not os.path.ecists(path):
        os.mkdir(path)

    degrees = Degree.objects.all()

    for degree in degrees:
        path = 'cache/curso/' + degree.code
        if not os.path.exists(path):
            os.mkdir(path)
            generate_degree_data(degree)


def generate_degree_data(degree, path):
    average_graduation = average_graduation(degree) # media_formandos
    dic = merge_dicts(graph_average_ira(degree), graph_average_ira_evasion_semester(degree), graph_average_ira_graduation(degree), ['average_ira', 'semester_evasion', 'graduation'])
'''
    degree_data = {
        'time_graduation': average_time_to_graduation_degree(degree),
        'graduation_rate': average_graduation[0],
        'student_amount': average_graduation[1],
        'failure_rate': averag
        'ira_average':

    }
'''
if __name__ == '__main__':
    main()
