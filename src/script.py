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
        generate_degree_data(degree, path)
        generate_student_data(degree, path)
        generate_student_list_data(degree, path)
        generate_admission_data(degree, path)
        generate_list_admission_data(degree, path)    
        generate_course_data(degree, path)
        generate_course_general_data(degree, path)
        generate_cepe9615(degree, path)

def generate_degree_data(degree, path):
    average_graduation = average_graduation(degree) # media_formandos
    dic = merge_dicts(graph_average_ira(degree), graph_average_ira_evasion_semester(degree), graph_average_ira_graduation(degree), ['average_ira', 'semester_evasion', 'graduation'])
    degree_data = {
        'time_graduation': average_time_graduation_degree(degree),
        'graduation_rate': average_graduation[0],
        'student_amount': average_graduation[1],
        'failure_rate': average_general_failure_standard_deviation(degree),
        'failure_actives': average_actives_failure_standard_deviation(degree),
        'ira_average': calculate_average_general_ira_standard_deviation(degree),
        'ira_actives': calculate_average_actives_ira_standard_deviation(degree),
        'evasion_rate': calculate_general_evasion(degree),
        'average_ira_graph': json.dumps(sorted(dic.items())),
        'evasion_graph': json.dumps(sorted(graph_evasion(degree).items())),
        'retirement': student_retirement(degree),
        'amount_student_actives': amount_student_actives(degree),
        'total_students': Student.objects.filter(admission__degree = degree).count(),
        'amount_locking': student_lock(degree),
        'gradueted': student_gradueted(degree)
    }

    with io.open(path + '/degree.json', 'w', encoding='utf8') as output:
        str_ = json.dumps(degree_data, indent = 4, sort_keys = True,
                   separators=(',',': '), ensure_ascii = False)
        output.write(to_unicode(str_))
if __name__ == '__main__':
    main()
