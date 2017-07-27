# -*- coding: utf-8 -*-
from .models import Degree
from admission.models import Admission
from klass.models import Klass, StudentKlass
import numpy as np
import math

SITUATIONS_COURSE_COMPLETED = ( # Situacoes cursadas ate o fim
    u'Reprovado por nota',
    u'Aprovado',
    u'Aprovado Adiantamento',
    u'Reprovado por Frequência',
    u'Reprovado sem note',
)

SITUATIONS_DISAPPROVALS = ( # Situacoes reprovacao
    u'Reprovado por nota',
    u'Reprovado por Frequência',
    u'Reprovado sem nota',
)

SITUATION_COMPLETED = (
    u'Aprovado',
    u'Aprovado Adiantamento',
    u'Aprov Conhecimento',
    u'Dispensa de Disciplinas (com nota)',
    u'Dispensa de Disciplinas (sem nota)',
#    u'Equivalência de Disciplina'
)


SITUATION_NO_EVASION = (
    u'Sem evasão',
    u'Formatura',
    u'Reintegração',
)

SITUATION_LOCKING = (
    u'Trancamento Total',
    u'Trancamento Administrativo'
)


def student_lock(degree):
    students = Student.objects.filter(admission__degree = degree, 
                   evasion_form = "Sem evasão")
    lockings = StudeintKlass.objects.filter(student__in = students,
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
