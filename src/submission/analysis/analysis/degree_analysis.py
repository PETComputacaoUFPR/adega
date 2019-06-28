import math
import json
import pandas as pd
import numpy as np
from submission.analysis.utils.situations import Situation, EvasionForm
from submission.analysis.utils.utils import IntervalCount, save_json
from submission.analysis.analysis.student_analysis import *

from submission.analysis.analysis.student_analysis import StudentAnalysis 


def average_graduation(df):
    """
    Calculates the ratio of students who have already graduated
    to number of students on the original dataframe.

    Returns
    -------
    float

    Examples
    --------
    13.395865237366003
    """
    students = df['MATR_ALUNO'].drop_duplicates()
    total_student = students.shape[0]
    total_graduate = students.loc[df.FORMA_EVASAO == EvasionForm.EF_FORMATURA].shape[0]
    return total_graduate / total_student


def general_failure(df):
    """

    Returns
    -------

    Examples
    --------
    """
    affect_ira = df[df.SITUACAO.isin(Situation.SITUATION_AFFECT_IRA)]
    failures = affect_ira[affect_ira.SITUACAO.isin(Situation.SITUATION_FAIL)]

    average = failures.shape[0] / affect_ira.shape[0]

    return average
    # student_courses = affect_ira.groupby(['MATR_ALUNO'], as_index=False)\
    #                             .aggregate({'SITUACAO': 'count'})
    # student_failures = failures.groupby(['MATR_ALUNO'], as_index=False)\
    #                            .aggregate({'SITUACAO': 'count'})

    # merged = pd.merge(student_courses, student_failures, on=['MATR_ALUNO'])
    # merged.columns = ['MART_ALUNO', 'FEITAS', 'REPROVADO']
    # variance = merged['REPROVADO'].div(merged['FEITAS']).sub(average)\
    #                                   .pow(2).sum() / merged.shape[0]
    # standard_deviation = math.sqrt(variance)

    # return (average, standard_deviation)


def current_students_failure(df):
    fixed = df.loc[(df.FORMA_EVASAO == EvasionForm.EF_ATIVO)]
    affect_ira = fixed[fixed.SITUACAO.isin(Situation.SITUATION_AFFECT_IRA)]
    failures = affect_ira[affect_ira.SITUACAO.isin(Situation.SITUATION_FAIL)]

    average = failures.shape[0] / affect_ira.shape[0]

    return average
    # student_courses = affect_ira.groupby(['MATR_ALUNO'], as_index=False)\
    #                             .aggregate({'SITUACAO': 'count'})
    # student_failures = failures.groupby(['MATR_ALUNO'], as_index=False)\
    #                            .aggregate({'SITUACAO': 'count'})

    # merged = pd.merge(student_courses, student_failures, on=['MATR_ALUNO'])
    # merged.columns = ['MART_ALUNO', 'FEITAS', 'REPROVADO']
    # variance = merged['REPROVADO'].div(merged['FEITAS']).sub(average)\
    #                                   .pow(2).sum() / merged.shape[0]
    # standard_deviation = math.sqrt(variance)
    # return (average, standard_deviation)

def general_ira(student_analysis):
    iras = np.array(list(student_analysis.ira_alunos().values()))

    return (iras.mean(), iras.std())

def current_ira(df, student_analysis):
    ano_grade = int(df.loc[df['NUM_VERSAO'].idxmax()]['NUM_VERSAO'])
    fixed = df.loc[(df['NUM_VERSAO'] == ano_grade)]
    iras = np.array(list(student_analysis.ira_alunos(df = fixed).values()))
 
    return (iras.mean(), iras.std())

def current_students_ira(df, student_analysis):
    fixed = df.loc[(df.FORMA_EVASAO == EvasionForm.EF_ATIVO)]
    iras = np.array(list(student_analysis.ira_alunos(df = fixed).values()))

    return (iras.mean(), iras.std())

def general_evasion_rate(df):
    students = df['MATR_ALUNO'].drop_duplicates()
    total_student = students.shape[0]
    total_evasion = students.loc[(df.FORMA_EVASAO != EvasionForm.EF_ATIVO) & (df.FORMA_EVASAO != EvasionForm.EF_FORMATURA) & (df.FORMA_EVASAO != EvasionForm.EF_REINTEGRACAO)].shape[0]

    return total_evasion / total_student

def current_evasion_rate(df):
    ano_grade = int(df.loc[df['NUM_VERSAO'].idxmax()]['NUM_VERSAO'])
    students = df.loc[(df['NUM_VERSAO'] == ano_grade)]
    students = students['MATR_ALUNO'].drop_duplicates()
    total_student = students.shape[0]
    total_evasion = students.loc[(df.FORMA_EVASAO != EvasionForm.EF_ATIVO) & (df.FORMA_EVASAO != EvasionForm.EF_FORMATURA) & (df.FORMA_EVASAO != EvasionForm.EF_REINTEGRACAO)].shape[0]

    return total_evasion / total_student

def average_graduation_time(df):
    """
   
   
    Returns
    -------
    float

    Examples
    --------
    5.3741640468705345 (years?)
    """
    students = df.drop_duplicates('MATR_ALUNO')
    graduates = students.loc[(df.FORMA_EVASAO == EvasionForm.EF_FORMATURA)]
    total_graduate = graduates.shape[0]
    average_time = 0
    year_end = int(df['ANO'].max())
    for index, row in graduates.iterrows():
        if pd.notnull(row['ANO_EVASAO']):
            year_end = int(row['ANO_EVASAO'])
            try:
                evasion_dt = int(row["DT_EVASAO"].split("/")[1])
                if(evasion_dt > 7):
                    semester_end = 2
                else:
                    semester_end = 1
            except (ValueError, AttributeError):
                try:
                    semester_end = int(row['SEMESTRE_EVASAO'])
                except (ValueError, AttributeError):
                    # TODO: Some students will be not considered
                    # The interface must inform the user this information
                    # and how many students wasnt considered
                    continue

        year = int(row['ANO_INGRESSO'])
        semester = int(row['SEMESTRE_INGRESSO'])
        difference = 2 * (year_end - year) + (semester_end - semester) + 1
        average_time += difference
    average_time /= total_graduate
    average_time /= 2
    return average_time

def total_students(df):
    return df.drop_duplicates('MATR_ALUNO').shape[0]

def current_total_students(df):
    return df.loc[(df.FORMA_EVASAO == EvasionForm.EF_ATIVO)].drop_duplicates('MATR_ALUNO').shape[0]

def taxa_abandono(df):
    students = df['MATR_ALUNO'].drop_duplicates()
    total_student = students.shape[0]
    total_abandono = students.loc[(df.FORMA_EVASAO == EvasionForm.EF_ABANDONO)].shape[0]
    return total_abandono / total_student



#The following 3 functions are auxiliar to make the 3 dicts the function merge_dicts receives 
def average_ira_graph(student_analysis):
    dic = build_dict_ira_medio(student_analysis.ira_alunos())
    return dic

def current_students_average_ira_graph(df, student_analysis):
    alunos_se = df.loc[(df.FORMA_EVASAO == EvasionForm.EF_ATIVO)]    
    dic_se = build_dict_ira_medio(student_analysis.ira_alunos(df = alunos_se))
    return dic_se

def graduates_average_ira_graph(df, student_analysis):
    alunos_for = df.loc[(df.FORMA_EVASAO == EvasionForm.EF_FORMATURA)]

    dic_for = build_dict_ira_medio(student_analysis.ira_alunos(df = alunos_for))

    return dic_for



def period_evasion_graph(df):
 
    di_qtd = {}
    dic = {}
    evasions_total = 0

    # Discover the minimum and maximum values for year
    year_start = int(df['ANO'].min())
    year_end = int(df['ANO'].max()) + 1

    students = df.drop_duplicates()


    # Iterate between all semester/year possible
    for year in range(year_start, year_end):
        for semester in range(1, 3):
            
            # Filter the rows and mantain only the registers
            # that match with year and semester of this iteration
            evasions = students.loc[
                (df['ANO_EVASAO'] == str(year)) &
                (df['SEMESTRE_EVASAO'] == str(semester))
            ]

            # Count only one row per student by removing
            # all duplicate rows with same MATR_ALUNO
            # and keeping the first row founded
            # Than, get the number of rows computed
            evasions = evasions.drop_duplicates(
                subset= "MATR_ALUNO",
                keep='first'
            ).shape[0]

            # Name of string on dictionary generated
            date = str(year) + ' {}º Período'.format(semester)
            di_qtd[date] = evasions

            # Count the total of evasions identified, that will be
            # used to compute the rate
            evasions_total += evasions

    # If at least one evasion was computed
    if evasions_total:
        # Compute the ratio of evasion per
        # semester and name the attributes
        for di in di_qtd:
            qtd = di_qtd[di]
            dic[di] = {'qtd': qtd, 'taxa': (float(qtd)/evasions_total)*100}
    
    return dic

def evasion_per_period_graph(df):
    """
    Build the dict for the graph 
    that displays how many people evades in each period (1-8)
    
    Filter df for evaded people and the needed columns
    Divide df per student 
    and apply current_period() to each student's dataframe 
    Calculates the times current_period() returns period x
    
    Parameters
    ----------
    df : DataFrame

    Returns 
    -------
    dict of {int: int}

        evasions_period = {
            period 1: number of people evaded,
            period 2: number of people evaded,
            ...
            }

    Examples
    --------
        {1:56, 2:63, ..., 8:2}

    """
    # Filter df for evaded people 
    rows = (df.FORMA_EVASAO != EvasionForm.EF_ATIVO) & (df.FORMA_EVASAO != EvasionForm.EF_FORMATURA)  & (df.FORMA_EVASAO != EvasionForm.EF_REINTEGRACAO)
    cols = ["MATR_ALUNO", "NUM_VERSAO_x", "COD_ATIV_CURRIC", "SITUACAO"]
    evaded_students = df.loc[rows, cols] 

    # print (evaded_students)
    StudentAnalysis.current_period(evaded_students)

    evasions_period = defaultdict(int)

    # print(evasions_period)
    return evasions_period

def build_dict_ira_medio(alunos):
    dic = {"00-4.9":0, "05-9.9":0, "10-14.9":0, "15-19.9":0, "20-24.9":0, "25-29.9":0, "30-34.9":0,
           "35-39.9":0, "40-44.9":0, "45-49.9":0, "50-54.9":0, "55-59.9":0, "60-64.9":0, "65-69.9":0,
           "70-74.9":0, "75-79.9":0, "80-84.9":0, "85-89.9":0, "90-94.9": 0,"95-100":0}

    iras = []
    for index, row in alunos.iterrows():
        if(row['MEDIA_FINAL'] is not None):
            iras.append(row['MEDIA_FINAL'])

    for d in dic:
        aux = d.split('-')
        v1 = float(aux[0])
        if (v1 == 0.0):
            v1 += 0.01
        v2 = float(aux[1])
        dic[d] = sum((float(num) >= v1) and (float(num) < v2) for num in iras)

    return dic


def build_dict_ira_medio(iras):
    """
    Uses numpy.histogram to create the intervals of iras (dict's keys)
    and counts how many iras on each interval (dict's values)     

    Parameters
    -------
    iras = {grr: ira, 
            grr: ira,
            ...}

    Returns
    -------
    dict = {'0.50-0.55': 91, 
            '0.55-0.60': 98,   
            '0.05-0.10': 38, 
            '0.65-0.70': 90, 
            ... }
    """
    iras_values = list(iras.values())

    # keys = ira intervals borders
    # values = quantity of students in the interval 
    values, keys = np.histogram(iras_values, bins=20, range=(0,1))
    dict = {}
    for i, count in enumerate(values):
        inf = keys[i]
        sup = keys[i+1]
        convert_key = "{:.2f}".format(inf) + "-" + "{:.2f}".format(sup)
        dict[convert_key] = int(count)
    return dict


def merge_dicts(dict1, dict2, dict3):
    """
    Makes a single dict for the STUDENTS per IRA graph.

    Takes 3 dictionaries whose keys are IRA intervals and merge them.
    Each IRA interval got as value another dictionary with 3 itens:
    number of all students with that IRA range;
    number of active students with that IRA range;
    number of graduated students with that IRA range;

    Parameters
    ----------
    3 x dicts = {'0.50-0.55': 91, 
                 '0.55-0.60': 98,
                 ...}

    Returns
    -------
        {'05-9.9': {'sem_evasao': 9,
                    'formatura': 3,
                    'ira_medio': 43},
        '10-14.9': {'sem_evasao': 12,
                    'formatura': 7,
                    'ira_medio': 37},
        ...}
    """
    dict_out = {}
    for key, value in dict1.items():
        v2 = dict2[key] if key in dict2 else None
        v3 = dict3[key] if key in dict3 else None
        dict_out[key] = {
            'total': value,
            'sem_evasao': v2,
            'formatura': v3
        }
    return dict_out


def build_degree_json(path,df,student_analysis):
    dic = merge_dicts(
        average_ira_graph(student_analysis),
        current_students_average_ira_graph(df, student_analysis),
        graduates_average_ira_graph(df, student_analysis)
    )
      
    degree_json = {
        "ira_medio_grafico": sorted(dic.items()),
        "evasao_grafico": json.dumps(sorted(period_evasion_graph(df).items())),
        "ira_atual": current_students_ira(df, student_analysis),
        "ira_medio": general_ira(student_analysis),
        "qtd_alunos": total_students(df),
        "qtd_alunos_atuais": current_total_students(df),
        "taxa_evasao": general_evasion_rate(df),
        "taxa_formatura": average_graduation(df),
        "taxa_reprovacao": general_failure(df),
        "taxa_reprovacao_atual": current_students_failure(df),
        "tempo_formatura": average_graduation_time(df),
        "evasao_grafico2": evasion_per_period_graph(df),
    }

    save_json(path+"/degree.json", degree_json)

    # with open(path+"/degree.json",'w') as f:
    #     f.write(json.dumps(degree_json,indent=4))
