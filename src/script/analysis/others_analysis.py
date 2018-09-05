import numpy as np
import pandas as pd 
from script.utils.situations import *

def student_three_fails_subject(df):
    df = df[df['SITUACAO'].isin(Situation.SITUATION_FAIL)]
    df = df[(df['FORMA_EVASAO'] == EvasionForm.EF_ATIVO)]
    students = df.groupby(["NOME_PESSOA", "MATR_ALUNO"])
    names = {}
    for student in students:
        subjects = student[1].groupby("COD_ATIV_CURRIC")
        for subject in subjects:
            if subject[1].shape[0] >= 3:
                names[student[0][0]] = student[0][1]
                break
    return names
