# -*- coding: utf-8 -*-
from .models import Degree
from admission.models import Admission
from klass.models import Klass, StudentKlass
import numpy as np
import math


def average_graduation(degree): # media_formandos
    pass

def average_time_graduation_degree(degree): # tempo_medio_formatura_curso
    pass

def average_general_failure_standard_deviation(degree): # media_reprovacao_geral_desvio_padrao
    pass

def average_actives_failure_standard_deviation(degree): # media_reprovacao_alunos_cursando_desvio_padrao
    pass

def calculate_average_general_ira_standard_deviation(degree): # calcular_ira_medio_geral_desvio_padrao
    pass

def calculate_average_actives_ira_standard_deviation(degree): # calcular_ira_medio_atual_desvio_padrao
    pass

def calculate_general_evasion(degree): # calcular_evasao_geral
   pass

def graph_evasion(degree): # grafico_periodo
    admissions = Admission.objects.filter(degree = degree)
    dict_amount = {}
    dic = {}
    evasion = 0

    for admission in admissions:
        year = admission.year
        semester = admission.semester
        index_semester_evasion = 0

def student_retirement(degree): # jubilamento_alunos
    year = degree.report_year
    semester = degree.report_semester
    curriculum = Curriculum.objects.filter(degree = degree)
    retirement = ((Curriculum.get_amount_of_semesters(curriculum) + 1) / 2) * 1.5
    year = int(year - retirement)
    students = Student.objects.filter(admission__degree = degree,
                   admission__year = year, admission__semester = semester,
                   evasion_form = "Sem evasão").count()

    return students

def amount_students_actives(degree): # quantidade_alunos_atual
    pass

def student_lock(degree): # trancamento_alunos
    students = Student.objects.filter(admission__degree = degree, 
                   evasion_form = "Sem evasão")
    lockings = StudentKlass.objects.filter(student__in = students,
                   situation__in = SITUATION_LOCKING)

    previous_student = None
    previous_year = 0
    previous_semester = 0
    amount_locking = 0

    for locking in lockings:
        if previous_student is not None and previous_student.grr == locking.student.grr and previous_year == locking.klass.year and previous_semester == locking.klass.semester:
            continue

        locked = True
        locking_year = locking.klass.year
        locking_semester = locking.klass.semester
        student_klasses = StudentKlass.objects.filter(student = locking.student,
                              klass__year__gte = locking_year)

        for sk in student_klasses:
            if sk.situation not in SITUATION_LOCKING:
                if sk.klass.year > locking_year:
                    if sk.klass.semester >= locking_semester:
                        locked = False
                else:
                    if sk.klass.semester > locking_semester:
                        locked = False

        if not locked:
            amount_locking += 1

        previous_student = locking.student
        previous_year = locking.klass.year
        previous_semester = locking.klass.semester

    return amount_locking

def student_gradueted(degree): # formando_alunos
    pass
