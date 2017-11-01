import sys
import os
import time
import math

from datetime import timedelta
from pathlib import Path
from utils.utils import build_path
from analysis.degree_analysis import *
from analysis.student_analysis import *

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
    generate_degree_data(path, dataframe)
    generate_student_data(path,dataframe)
#    generate_student_list(path)
#    generate_admission_data(path)
#    generate_admission_list(path)
#    generate_course_data(path)
#    generate_course_general_data(path)

def generate_degree_data(path, dataframe):
    average_graduation(dataframe)
    general_failure(dataframe)
    general_ira(dataframe)
    total_evasion_rate(dataframe)
    average_graduation_time(dataframe)
    pass

def generate_student_data(path,dataframe):
    #~ print(aluno_turmas(dataframe))
    #~ print(indice_aprovacao_semestral(dataframe))
    #~ print("2007/1" in ira_por_quantidade_disciplinas(dataframe)["GRR20066955"])
    #~ print(ira_semestra(dataframe)["GRR20079775"])
    #~ aluno_turmas(dataframe)
    #~ indice_aprovacao_semestral(dataframe)
    #~ ira_por_quantidade_disciplinas(dataframe)
    #~ ira_semestra(dataframe)
    #~ periodo_pretendido(dataframe)
    #~ print(periodo_real(dataframe))
    print(posicao_turmaIngresso_semestral(dataframe))
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
