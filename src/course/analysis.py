from __future__ import division
from student.models import Student
from klass.models import *
from admission.models import Admission
from course.models import *
from degree.models import *
from datetime import datetime
from student.analysis import *

import math

def average_grade(klasses): # calcular_nota_media(turmas)
    grade = 0
    amount_student = 0
    for klass in klasses:
        student_klasses = StudentKlass.objects.filter(klass = klass,
            situation__in = SITUATION_COURSE_VALID_GRADE)
        for student_klass in student_klasses:
            if student_klass.grade is not None:
                grade += student_klass.grade
                amount_student += 1

    if amount_student == 0:
        return -1
    else:
        return grade / amount_student

def average_grade_standard_deviation(klasses): # calcular_nota_media_desvio_padrao
    average_grade = average_grade(klasses)
    amount_student = 0
    variance = 0
    for klass in klasses:
        student_klasses = StudentKlass.objects.filter(klass = klass,
            situation__in = SITUATION_COURSE_VALID_GRADE)
        for student_klass in student_klasses:
            if student_klass.grade is not None:
                variance += math.pow(student_klass.grade - average_grade, 2)
                amount_student += 1

    if amount_student == 0:
        return -1

    standard_deviation = math.sqrt(variance/amount_student)
    return (average_grade, standard_deviation)

def average_grade_last_year(klasses): # calcular_nota_media_ultimo_ano
    grades = 0
    amount_student = 0
    now = datetime.now()
    for klass in klasses:
        if klass.year == (now.year - 1):
            student_klasses = StudentKlass.objects.filter(klass = klass)
            for student_klass in student_klasses:
                if student_klass.grade is not None:
                    grades += student_klass.grade
                    amount_student += 1

    if amount_student == 0:
        return -1

    return grades / student_amount

def average_grade_last_year_standard_deviation(klasses): # calcular_nota_media_ultimo_ano_desvio_padrao
    average_grade = average_grade_last_year(klasses)
    if average_gradde == -1:
        return (-1, -1)
    amount_student = 0
    variance = 0
    now = datetime.now()
    for klass in klasses:
        if klass.year == (now.year - 1):
            student_klasses = StudentKlass.objects.filter(klass = klass)
            for student_klass in student_klasses:
                if student_klass.grade is not None:
                    variance += math.pow(student_klass.grade - average_grade, 2)
                    amount_student += 1

    if amount_student == 0:
        return (-1,-1)

    standard_deviation = math.sqrt(variance / amount_student)

    return (average_grade, standard_deviation)

#def absolute_pass_rate(klasses): # calcular_taxa_reprovacao_absoluta

def frequency_failure(klasses): # calcular_taxa_reprovacao_frequencia
    amount_failure = 0
    amounte_student = 0
    for klass in klasses:
        student_klasses = StudentKlass.objects.filter(klass = klass)
        for student_klass in student_klasses:
            if student_klass.situation is not None:
                if student.situation == "Reprovado por Frequência":
                    amount_failure += 1
                amount_student += 1

    if amount_student == 0:
        return -1

    amount_failure *= 100
    return amount_failure / amount_student

