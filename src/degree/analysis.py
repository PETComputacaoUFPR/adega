# -*- coding: utf-8 -*-
from .models import Degree
from student.analysis import *
from student.models import Student
from admission.analysis import *
from admission.models import Admission
from klass.models import Klass, StudentKlass
from utils.data import *
import numpy as np
import math


def average_graduation(degree): # media_formandos
    student_list = Student.objects.filter(admission__degree = degree)
    total_student = student_list.count()
    graduate = student_list.filter(evasion_form = "Formatura").count()
    graduation_rate = graduate / total_student * 100

    return [graduation_rate, total_student]

def average_time_graduation_degree(degree): # tempo_medio_formatura_curso
    students = Student.objects.filter(admission__degree = degree)
    graduated = students.filter(evasion_form = "Formatura")
    graduated_amount = graduated.count()
    average_time = 0

    for g in graduated:
        print(g.get_time_in_degree())
        average_time += g.get_time_in_degree()

    average_time /= graduated_amount
    average_time /= 2

    return average_time

def average_general_failure(students):
    courses = 0
    failures = 0
    for student in students:
        student_klasses = StudentKlass.objects.filter(student=student)
        for sk in student_klasses:
            courses += 1
            if sk.situation in SITUATIONS_FAILURE:
                failures += 1
    return failures / courses * 100

def average_general_failure_standard_deviation(degree): # media_reprovacao_geral_desvio_padrao
    students = Student.objects.filter(admission__degree = degree)
    average_failure = average_general_failure(students)
    variance = 0
    
    for student in students:
        courses = 0
        failures = 0
        student_klasses = StudentKlass.objects.filter(student=student)

        for sk in student_klasses:
            courses += 1
            if sk.situation in SITUATIONS_FAILURE:
                failures += 1

        variance += math.pow((failures / courses) - average_failure, 2)

    variance /= students.count()
    standard_deviation = math.sqrt(variance)

    return [average_failure, standard_deviation]

def average_actives_failure(students):
   courses = 0
   failures = 0
   for student in students:
       student_klasses = StudentKlass.objects.filter(student=student)
       for sk in student_klasses:
           courses += 1
           if sk.situation in SITUATIONS_FAILURE:
               failures += 1
   return failures / courses * 100

def average_actives_failure_standard_deviation(degree): # media_reprovacao_alunos_cursando_desvio_padrao
    students = Student.objects.filter(admission__degree=degree, evasion_form = "Sem evasão")
    average_failure = average_actives_failure(students)
    variance = 0
    for student in students:
        courses = 0
        failures = 0
        student_klasses = StudentKlass.objects.filter(student=student)
        for sk in student_klasses:
             courses += 1
             if sk.situation in SITUATIONS_FAILURE:
                 failures += 1

        variance += math.pow(failures / courses - average_failure, 2)

    variance /= students.count()
    standard_deviation = math.sqrt(variance)

    return [average_failure, standard_deviation]

def calculate_average_general_ira_standard_deviation(degree): # calcular_ira_medio_geral_desvio_padrao
    students = Student.objects.filter(admission__degree = degree, ira__isnull = False)
    average = 0
    amount = students.count()
    for student in students:
        average += student.ira
        
    return average / amount

def calculate_average_actives_ira_standard_deviation(degree): # calcular_ira_medio_atual_desvio_padrao
    students = Student.objects.filter(admission__degree = degree, evasion_form = "Sem evasão", ira__isnull = False)
    average = 0
    amount = students.count()
    for student in students:
         average += student.ira

    return average / amount

def calculate_general_evasion(degree): # calcular_evasao_geral
   students = Student.objects.filter(admission__degree = degree)
   student_amount = students.count()
   evasion_amount = students.exclude(evasion_form__in = SITUATION_NO_EVASION).count()
   
   return 0 if student_amount == 0 else evasion_amount / student_amount

def graph_evasion(degree): # grafico_periodo
    admissions = Admission.objects.filter(degree = degree)
    dict_amount = {}
    dic = {}
    evasion = 0

    for admission in admissions:
        year = admission.year
        semester = admission.semester
        evasion_semester_rate = calculate_evasion_rate_semester(admission)
        for esr in evasion_semester_rate:
            date = esr.split('/')
            year_s = 2*(int(date[0]) - year)
            if int(date[1]) - semester < 0:
                semester_s = 1
            else:
                semester_s = int(date[1]) - semester

            if year_s + semester_s + 1 > 8:
                continue

            date = '{}º Período'.format(year_s + semester_s + 1)
            if date not in dict_amount:
                dict_amount[date] = 0
            dict_amount[date] += evasion_semester_rate[esr]['amount_evasion']
            evasion += evasion_semester_rate[esr]['amount_evasion']

    for da in dict_amount:
        amount = dict_amount[da]
        dic[da] = {'amount': amount, 'rate': (amount/evasion)*100}

    return dic

def graph_average_ira(degree): # grafico_ira_medioi
    students = Student.objects.filter(admission__degree = degree)
    dic = build_dict_average_ira(students)

    return dic

def graph_average_ira_evasion_semester(degree): # grafico_ira_medio_sem_evasao
    students = Student.objects.filter(admission__degree = degree, evasion_form = 'Sem evasão')
    dic = build_dict_average_ira(students)

    return dic

def graph_average_ira_graduation(degree): # grafico_ira_medio_formatura
    students = Student.objects.filter(admission__degree = degree, evasion_form = "Formatura")
    dic = build_dict_average_ira(students)

    return dic

def build_dict_average_ira(students):
    dic = {"00-4.9":0, "05-9.9":0, "10-14.9":0, "15-19.9":0, "20-24.9":0, "25-29.9":0, "30-34.9":0,
           "35-39.9":0, "40-44.9":0, "45-49.9":0, "50-54.9":0, "55-59.9":0, "60-64.9":0, "65-69.9":0,
           "70-74.9":0, "75-79.9":0, "80-84.9":0, "85-89.9":0, "90-94.9": 0,"95-100":0}

    iras = []
    for student in students:
        if student.ira is not None:
            iras.append(student.ira)

    for d in dic:
        aux = d.split('-')
        v1 = float(aux[0])
        if v1 == 0.0:
            v1 += 0.01
        v2 = float(aux[1])
        dic[d] = sum((float(num) >= v1) and (float(num) < v2) for num in iras)

    return dic

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

def amount_student_actives(degree): # quantidade_alunos_atual
    amount_student = Student.objects.filter(admission__degree = degree, evasion_form = "Sem evasão").count()
    return amount_student

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
