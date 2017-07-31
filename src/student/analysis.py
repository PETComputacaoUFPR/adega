# -*- coding:utf-8 -*-
from student.models import Student
from klass.models import *
from admission.models import Admission
from degree.models import *
from datetime import datetime
from django.db.models import Max
from utils.data import *

def pass_amount(student_klasses): # calcular_indice_aprovacao
    amount_pass = 0
    amount_courses = 0
    for student_klass in student_klasses:
        if student_klass.situation in SITUATIONS_COURSE_COMPLETED:
            amount_courses += 1
            if student_klass.situation in SITUATION_PASS:
                amount_pass += 1


    return -1 if amount_courses == 0 else amount_pass

def pass_rate(student_klasses): # indice_aprovacao
    amount_pass = 0
    amout_courses = 0
    for sk in student_klasses:
        if sk.situation in SITUATIONS_COURSE_COMPLETED:
            amount_courses += 1
            if sk.situation in SITUATION_PASS:
                amount_pass += 1
    return -1 if amount_courses == 0 else amount_pass / amount_courses

def semester_pass_rate(student): # calcular_indice_aprovacao_semestral
    index = {}
    amount_semesters = student.get_time_in_degree()
    year = student.admission.year
    semester = student.admission.semester 

    for i in range(0, amount_semesters):
        #semester_student_klass = student.studentklass_set.filter(klass__year = year, klass__semester = semester
        #semester_index = pass_amount
        semester_index = student.studentklass_set.filter(klass__year = year, klass__semester = semester, situation__in = SITUATION_PASS).count()

        if semester_index > 0:
            key = "{}/{}".format(year, semester)
            index[key] = semester_index

        semester = (semester % 2) + 1
        semester += semester % 2

    return index

def get_student_courses_completed(student_klasses):
    student_courses_completed = []

    for student_klass in student_klasses:
        
        if student_klass.situation in SITUATIONS_COURSE_COMPLETED:
            student_courses_completed.append(student_klass)

    return student_courses_completed

def get_amount_courses_completed(student):
    amount = {}

    amount_semesters = student.get_time_in_degree()
    year = student.admission.year
    semester = student.admission.semester

    for i in range(0, amount_semesters):
        student_klass_semester = student.studentklass_set.filter(klass__year = year, klass__semester = semester)
        key = "{}/{}".format(year, semester)
        amount[key] = len(get_student_courses_completed(student_klass_semester))
        semester = (semester % 2) + 1
        year += semester % 2

    return amount

def calculate_ira(student_klasses):
    ira = 0
    total_workload = 0

    for student_klass in student_klasses:
        if student_klass.situation in SITUATION_AFFECT_IRA:
            workload = student_klass.klass.course.workload
            total_workload += workload
            ira += student_klass.grade * workload

    if total_workload == 0:
        return -1
    else:
       ira /= total_workload

    return ira / 100

def get_ira_semester(student):
    iras = {}

    amount_semesters = student.get_time_in_degree()
    year = student.admission.year
    semester = student.admission.semester
    
    for i in range(0, amount_semesters):
        student_klass_semester = student.studentklass_set.filter(klass__year = year, klass__semester = semester)
        semester_ira = calculate_ira(student_klass_semester)

        if semester_ira >= 0:
            key = "{}/{}".format(year, semester)
            iras[key] = semester_ira

        semester = (semester % 2) + 1
        year += semester % 2

    return iras

def get_student_position(student):
    student_iras = get_ira_semester(student)
    positions = {}
    positions = positions.fromkeys(student_iras.keys())
    positions = {semester: {'position': 1, 'amount_student': 1} for semester, value in student_iras.items()}

    admission_students = Student.objects.filter(admission = student.admission).exclude(grr = student.grr)

    for admission_student in admission_students:
        iras = get_ira_semester(admission_student)
        for key in positions:
            if key in iras and iras[key] >= 0:
                positions[key]['position'] += 1
            positions[key]['amount_student'] += 1

    positions = {semester: value['position'] / value['amount_student'] for semester, value in positions.items()}

    return position

def ira_amount_courses(student):
    ira_semesters = get_ira_semester(student)
    amount_courses = get_amount_courses_completed(student)

    ira_amount_course = {}
    ira_amount_course = ira_amount_course.fromkeys(ira_semesters.keys())

    for ira_semester in ira_semesters:
        ira_amount_course[ira_semester] = [ira_semesters[ira_semester], amount_courses[ira_semester]]

    return ira_amount_course

def get_real_period(student, last_period = None):
    if last_period is None:
        last_period = student.curriculum.get_amount_of_semesters()

    real_period = 0
    period_completed = True
    while period_completed and real_period <= last_period:
        real_period += 1

        courses_period = student.current_grade.courses.filter(coursecurriculum__period = real_period)
        courses_passed_period = courses_period.filter(klass__studentklass__student = student, klass__studentkass__situation__in = SITUATION_CONCLUDED)
        period_completed = len(courses_passed_period) == len(courses_period)

    if real_period > last_period:
        return -1

    return real_period

def get_intended_period(student):
    amount_semester_student = student.get_time_in_degree()
    last_period_curriculum = student.current_curriculum.get_amount_of_semesters()

    if amount_semester_student > last_period_curriculum:
        return -1
    return amount_semester_student


