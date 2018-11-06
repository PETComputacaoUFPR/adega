"""This resolution from CEPE deals with the cases where studants might have
their academic record canceled."""
import numpy as np
import pandas as pd
import pprint
from script.utils.situations import *


fails_by_course = [10] # used at: student_three_fails_course
fails_by_semester = [6, 10] # used at: n_fails_semester
fails_by_freq = [3, 5, 7] # used at: n_fails_by_freq


pp = pprint.PrettyPrinter(indent=4)

# for x in LISTA_DISCIPLINA_REPROVACOES_CONTAGEM:
#     computa_lista_reprovacoes(reprovacoes=x)


def student_fails_course(df):
    """
    Lists of students that failed X, Y, Z ... times in the same course.
    X, Y, Z ... are declared in the list "fails_by_course" at the top of analysis.

    This function is inspired by CEPE 96/15 ART.9:
    Students with 3 fails in the same course would have their registration suspended.

    Parameters
    ----------
    df : DataFrame

    Returns
    -------
    dict of {int:dict}

			quantity={
			"3":{aluno1:GRR, aluno2:GRR, ...},
			"7":{aluno1:GRR, aluno2:GRR, ...},
			...
			}

    Examples
    --------
    "3" : {
	"José da Silva Carvalho": 20114027,
	"Pedro dos Santos" : 20152678,
        ...
    }

    "7" : {
	"José da Silva Carvalho": 20114027,
	"Pedro dos Santos" : 20152678,
        ...
}
    """
    # Filters based on the students that have failed at least once
    # and are still registered on the University
    df = df[df['SITUACAO'].isin(Situation.SITUATION_FAIL)]
    df = df[(df['FORMA_EVASAO'] == EvasionForm.EF_ATIVO)]
    # Creates a tuple with (specified informations, dataframe)
    students = df.groupby(["NOME_PESSOA", "MATR_ALUNO"])
    quantity = {}
    for times in fails_by_course:
        names = {}
        for student in students:
            # For each student that have failed, we will have a dataframe of
            # the student and in wich course they did fail
            courses = student[1].groupby("COD_ATIV_CURRIC")
            for course in courses:
                if course[1].shape[0] == times: #shape count the lines
                    names[student[0][0]] = student[0][1]
                    break

        quantity[str(times)] = names

    return quantity



def fails_semester (df):
    """
    Lists of students that failed X, Y, Z ... courses in the same semester.
    X, Y, Z ... are declared in the list "fails_by_semester" at the top.

    This function is inspired by CEPE 96/15 ART.9:
    Students with 3 fails in the semester would have their registration suspended.

    First this function filters students who are still registrered in the University
    and have failed courses.
    Then it creates a dictionary of semesters.
    Inside each semester there is a second dictionary of names and df with the failed courses
    This second dictionary will be turned into a list of names according to each N in fails_by_semester

    Parameters
    ----------
    df : DataFrame

    Returns
    -------
    dict of {int:dict}

        final_dict={
        "X":{semester1: list_of_students1, ...},
        "Y":{semester1: list_of_students1, ...},
        ...
        }

    Examples
    --------
        '4': {   (2001, '2o. Semestre'): [],
                     (2002, '1o. Semestre'): [],
                     (2002, '2o. Semestre'): [],
                     (2003, '1o. Semestre'): [],
                     (2004, '2o. Semestre'): [],
                     (2007, '1o. Semestre'): [],
                     (2007, '2o. Semestre'): [   (   'Carlos das Neves Vieira',
                                                     'GRR20073713'),
                                                 (   'Adriano Dias Barbosa',
                                                     'GRR20075214')],
                     (2008, '1o. Semestre'): [   (   'Anderson Silveira Alves',
                                                     'GRR20075297')],
    """
    people_studying_df = df[df['FORMA_EVASAO'] == EvasionForm.EF_ATIVO]
    failed_people_df = people_studying_df[people_studying_df['SITUACAO'].isin(Situation.SITUATION_FAIL)]
    failed_people_per_semester_grouped = failed_people_df.groupby(['ANO','PERIODO'])
    # semester_dict = { (2017/1): names_dict1, (2017/2): names_dict2, ...}
    # names_dict    = { (nome, grr): df, (nome. grr): df, ...)
    semester_dict = {}
    for semester in failed_people_per_semester_grouped:
        names_dict = {}
        student_grouped = semester[1].groupby(["NOME_PESSOA", "MATR_ALUNO"])
        for student in student_grouped:
            names_dict[student[0]] = student[1]
        semester_dict[semester[0]] = names_dict

    # final_dict = { N: semester_finaldict, ...}
    # semester_finaldict = { semester: list of students tha failed N courses in that semester}
    final_dict = {}
    for n in fails_by_semester:
        semester_finaldict = {}
        for semester in semester_dict:
            name_list = []
            for student in semester_dict[semester]:
                if semester_dict[semester][student].shape[0] == n:
                    name_list.append(student)
            semester_finaldict[semester] = name_list
        final_dict[str(n)] = semester_finaldict
    # pp.pprint (final_dict)
    return final_dict


def fails_by_freq(df):
    """
    Lists of students that failed a course X, Y, Z ... times, all of them by lack of frequency!
    X, Y, Z ... are declared in the list "fails_by_freq" at the top.

    This function is inspired by CEPE 96/15 ART.4:
    Students will be categorize with insuficient academic rendimento
    when failing 2 times a course

    First this function filters students who are still registrered in the University
    and have failed courses by lack of frequenecy.
    Then for each n in fails_by_freq, filters if a course repeat n times for a student

    Parameters
    ----------
    df : DataFrame

    Returns
    -------
    dict of {int: list of tuples}

        final_dict = {
                        "X":[   {student: student, course: course, ...},
                                {student: student, course: course, ...},
                        ... ]
                        "Y":[   {student: student, course: course, ...},
                                {student: student, course: course, ...},
                        ... ]
                ... }

    Examples
    --------
    { 5: [   ('António Cardoso Mendes', 'CI067'),
           ('Artur Lima Silva', 'CI068'),
           ...
           ('Ângelo Castro da Mota', 'CI237')],
    7: [   ('Daniel Gomes Martins', 'CI077'),
           ('Joaquim Rodrigues Carvalho', 'CI210'),
           ...
           ('Pietra Martins Moreira', 'CI210')]}
    """
    people_studying_df = df[df['FORMA_EVASAO'] == EvasionForm.EF_ATIVO]
    failedbyfreq = people_studying_df.loc[people_studying_df['SITUACAO'] == Situation.SITUATION_FAIL[1]]
    coursefailed_bystudent = failedbyfreq.groupby(["NOME_PESSOA", "MATR_ALUNO", "COD_ATIV_CURRIC"])
    final_dict = {}
    for n in fails_by_freq:
        final_dict[n] = []
        for fail in coursefailed_bystudent:
            if fail[1].shape[0] == n:
                final_dict[n].append((fail[0][0], fail[0][2]))
    pp.pprint (final_dict)
