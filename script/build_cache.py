import sys
import os
import time
import math

from datetime import timedelta
from pathlib import Path
from utils.utils import build_path
import analysis.degree_analysis as de_an
import analysis.student_analysis as st_an
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

    generate_student_data(path, dataframe)
#    generate_degree_data(path, dataframe)
#    generate_student_data(path)
#    generate_student_list(path)
#    generate_admission_data(path)
#    generate_admission_list(path)
#    generate_course_data(path)
#    generate_course_general_data(path)

def generate_degree_data(path, dataframe):
    de_an.average_graduation(dataframe)
    de_an.general_failure(dataframe)
    de_an.general_ira(dataframe)
    pass


def teste(d):
    temp = d.dropna(subset=['MEDIA_FINAL'])
    temp = temp[temp['MEDIA_FINAL'] <= 100]
    if not temp.empty:
        #print(temp[['MEDIA_FINAL', 'CH_TOTAL']])
        aux = np.sum(temp['MEDIA_FINAL']*temp['CH_TOTAL'])
        ch_total = np.sum(temp['CH_TOTAL']) * 100
        print(aux/ch_total)

def generate_student_data(path, dataframe):
#    student_df = dataframe.groupby('MATR_ALUNO')
    dataframe.students.aggregate(teste)
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
