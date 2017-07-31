# -*- coding:utf-8 -*-
from __future__ import division
from django.shortcuts import get_object_or_404
from django.db import models
from student.models import Student
from klass.models import *
from admission.models import Admission
from degree.models import *
from datetime import datetime
from utils.data import *
import collections
import json
import math

def calculate_average_ira(admission):
    students = admission.student_set.all()
    average = 0
    amount = 0
    for student in students:
        if student.ira is not None:
            average += student.ira
            amount += 1

    if amount == 0:
        return -1
    else:
        average /= n
        return average

def calculate_average_ira_standard_deviation(admission):
    average_ira = calculate_average_ira(admission)
    students = admission.student_set.all()
    variance = 0
    amount = 0

    for student in students:
        if student.ira is not None:
            variance += math.pow(aluno.ira - average_ira, 2)
            amount += 1

    if amount == 0:
        return -1
    else:
        variance /= n
        standard_deviation = math.sqrt(variance)
        return (average_ira, standard_deviation)

def calculate_ira_semester(admission, year, semester, amount_semesters):
    students = admission.student_set.all()
    average = 0
    amount = 0
   
    for student in students: 
        time = studnet.get_time_in_degree()
        if amount_semesters < time:
            amount_semesters = time

        student_klass_semester = student.studentklass_set.filter(klass__year = year, klass__semester = semester)
        ira_semester = calculate_ira(student_klass_semester)
        if ira_semester >= 0:
            average += ira_semester
            amount += 1

    if amount == 0:
        return -1
    else:
        return average/amount

def calculate_ira_semester_standard_deviation(average, admission, year, semester, amount_semesters):
    students = admission.student_set.all()
    variance = 0
    amount = 0

    for student in students:
        time = student.get_time_in_degree()
        if amount_semesters == time:
            amount_semesters = time
        student_klass_semester = student.studentklass_set.filter(klass__year = year, klass__semester = semester)
        ira_semester = calculate_ira(student_klass_semesters)

        if ira_semester >= 0:
            variance += math.pow(ira_semester - average, 2)
            amount += 1

    if amount == 0:
        return -1
    else:
        return math.sqrt(variancia/amount)

def calculate_average_ira_semester(admission):
    averages = {}
    students = admission.student_set.all()
    year = admission.year
    semester = admission.semester
    amount_semesters = 0
    for student in students:
        time = student.get_time_in_degree()
        if amount_semesters < time:
            amount_semesters = time

    for i in range(0, amount_semesters - 1):
        key = "{}/{}".format(year, semester)
        ira_average = calculate_ira_semester(admission, year, semester, amount_semesters)
        ira_standard_deviation = calculate_ira_semester_standard_deviation(ira_average, admission, year, semester, amount_semesters)
        averages[key] = [ira_average, ira_standard_deviation]

        semester = (semester % 2) + 1
        year += semester % 2

    ordered_dict = collections.OrderedDict(sorted(average.items()))
    return ordered_dict

def calculate_pass_rate_semester(students):
    semesters = {}
    total_semesters = {}
    new_semesters = {}
    temp_semesters = {}

def calculate_evasion_rate(admission):
    return

def calculate_evasion_rate_semester(admission):
    students = Student.objects.filter(admission = admission)

    total_amount = students.count()
    evasion_semester = {}

    for student in students.exclude(evasion_form__in=SITUATION_NO_EVASION):
        if student.evasion_year is None or student.evasion_semester is None:
            continue

        date = str(student.evasion_year) + "/" + str(student.evasion_semester)

        if date not in evasion_semester:
            evasion_semester[date] = {'amount_evasion': 1}
        else:
            evasion_semester[date]['amount_evasion'] += 1

    if total_amount != 0:
        for key in evasion_semester:
            evasion_semester[key]['rate'] = 100 * evasion_semester[key]['amount_evasion'] / total_amount
    else:
        for key in evasion_semester:
            evasion_semester[key]['rate'] = 0

    return evasion_semester
