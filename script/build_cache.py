import sys
import os
import time
import math

from datetime import timedelta
from pathlib import Path
from utils.utils import build_path
from analysis.degree_analysis import *

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

def build_cache(dataframe):
#    os.chdir("../src")
    path = "cache"
    build_path(path)   
    path += "/curso"
    build_path(path)

    generate_degree_data(path, dataframe)
    generate_student_data(path)
    generate_student_list(path)
    generate_admission_data(path)
    generate_admission_list(path)
    generate_course_data(path)
    generate_course_general_data(path)

def generate_degree_data(path, dataframe):
    average_graduation(dataframe)
    general_failure(dataframe)
    general_ira(dataframe)
    pass

def generate_student_data(path):
    pass

def generate_student_list(path):
    pass

def generate_admission_data(path):
    pass

def generate_admission_list(path):
    pass

def generate_course_data(path):
    pass

def generate_course_general_data(path):
    pass
