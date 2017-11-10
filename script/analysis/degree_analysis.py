import pandas as pd
import math
from utils.situations import Situation, EvasionForm


def average_graduation(df):
    total_student = df['MATR_ALUNO'].drop_duplicates().shape[0]
    total_graduate = df[df.FORMA_EVASAO == EvasionForm.EF_FORMATURA].shape[0]

    return total_graduate / total_student


def general_failure(df):
    affect_ira = df[df.SITUACAO.isin(Situation.SITUATION_AFFECT_IRA)]
    failures = affect_ira[affect_ira.SITUACAO.isin(Situation.SITUATION_FAIL)]

    average = failures.shape[0] / affect_ira.shape[0]

    student_courses = affect_ira.groupby(['MATR_ALUNO'], as_index=False)\
                                .aggregate({'SITUACAO': 'count'})
    student_failures = failures.groupby(['MATR_ALUNO'], as_index=False)\
                               .aggregate({'SITUACAO': 'count'})

    merged = pd.merge(student_courses, student_failures, on=['MATR_ALUNO'])
    merged.columns = ['MART_ALUNO', 'FEITAS', 'REPROVADO']
    variance = merged['REPROVADO'].div(merged['FEITAS']).sub(average)\
                                      .pow(2).sum() / merged.shape[0]
    standard_deviation = math.sqrt(variance)
    return (average, standard_deviation)


def general_ira(df):
    fixed = df[df.SITUACAO.isin(Situation.SITUATION_AFFECT_IRA)]
    fixed = fixed[fixed.MEDIA_FINAL <= 100]
    return (fixed.MEDIA_FINAL.mean(), fixed.MEDIA_FINAL.std())

def total_evasion_rate(df):
    students = df['MATR_ALUNO'].drop_duplicates()
    total_student = students.shape[0]
    total_evasion = students.loc[(df.FORMA_EVASAO != EvasionForm.EF_ATIVO) & (df.FORMA_EVASAO != EvasionForm.EF_FORMATURA) & (df.FORMA_EVASAO != EvasionForm.EF_REINTEGRACAO)].shape[0]

    return total_evasion / total_student

def average_graduation_time(df):
    graduates = df.loc[(df.FORMA_EVASAO == EvasionForm.EF_FORMATURA)]
    total_graduate = graduates.shape[0]
    average_time = 0
    year_end = int(df['ANO'].max())
    semester_end = graduates['PERIODO'].max()
    for index, row in graduates.iterrows():
        if pd.notnull(row['ANO_EVASAO']):
            year_end = int(row['ANO_EVASAO'])
            try: 
                semester_end = int(row['SEMESTRE_EVASAO'])
            except ValueError:
                semester_end = graduates['PERIODO'].max()
        year = int(row['ANO_INGRESSO'])
        semester = int(row['SEMESTRE_INGRESSO'])
        difference = 2 * (year_end - year) + (semester_end - semester) + 1
        average_time += difference
    average_time /= total_graduate
    average_time /= 2

    return average_time