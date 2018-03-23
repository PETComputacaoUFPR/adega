import pandas as pd
import math
import ujson as json
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


def current_students_failure(df):
    fixed = df.loc[(df.FORMA_EVASAO == EvasionForm.EF_ATIVO)]
    affect_ira = fixed[fixed.SITUACAO.isin(Situation.SITUATION_AFFECT_IRA)]
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

def current_ira(df):
    ano_grade = int(df.loc[df['NUM_VERSAO'].idxmax()]['NUM_VERSAO'])
    fixed = df.loc[(df['NUM_VERSAO'] == ano_grade)]
    fixed = fixed[fixed.SITUACAO.isin(Situation.SITUATION_AFFECT_IRA)]
    fixed = fixed[fixed.MEDIA_FINAL <= 100]
    return (fixed.MEDIA_FINAL.mean(), fixed.MEDIA_FINAL.std())

def current_students_ira(df):
    fixed = df.loc[(df.FORMA_EVASAO == EvasionForm.EF_ATIVO)]
    fixed = fixed[fixed.SITUACAO.isin(Situation.SITUATION_AFFECT_IRA)]
    fixed = fixed[fixed.MEDIA_FINAL <= 100]
    return (fixed.MEDIA_FINAL.mean(), fixed.MEDIA_FINAL.std())

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

def total_students(df):
    return df.drop_duplicates('MATR_ALUNO').shape[0]

def current_total_students(df):
    return df.loc[(df.FORMA_EVASAO == EvasionForm.EF_ATIVO)].drop_duplicates('MATR_ALUNO').shape[0]

def taxa_abandono(df):
    students = df['MATR_ALUNO'].drop_duplicates()
    total_student = students.shape[0]
    total_abandono = students.loc[(df.FORMA_EVASAO == EvasionForm.EF_ABANDONO)].shape[0]

    return total_abandono / total_student

def average_ira_graph(df):
    alunos = df.drop_duplicates('MATR_ALUNO')

    dic = build_dict_ira_medio(alunos)

    return dic

def current_students_average_ira_graph(df):
    alunos_se = df.loc[(df.FORMA_EVASAO == EvasionForm.EF_ATIVO)]
    alunos_se = alunos_se.drop_duplicates('MATR_ALUNO')

    dic_se = build_dict_ira_medio(alunos_se)

    return dic_se

def graduates_average_ira_graph(df):
    alunos_for = df.loc[(df.FORMA_EVASAO == EvasionForm.EF_FORMATURA)]
    alunos_for = alunos_for.drop_duplicates('MATR_ALUNO')

    dic_for = build_dict_ira_medio(alunos_for)

    return dic_for

def period_evasion_graph(df):
    di_qtd = {}
    dic = {}
    evasions_total = 0
    year_start = int(df['ANO'].min())
    year_end = int(df['ANO'].max()) + 1
    students = df.drop_duplicates()
    for year in range(year_start, year_end):
        for semester in range(1, 3):
            evasions = students.loc[(df['ANO_EVASAO'] == str(year)) & (df['SEMESTRE_EVASAO'] == str(semester))].shape[0]
            date = str(year) + ' {}º Período'.format(semester)
            di_qtd[date] = evasions
            evasions_total += evasions
    if evasions_total:
        for di in di_qtd:
            qtd = di_qtd[di]
            dic[di] = {'qtd': qtd, 'taxa': (qtd/evasions_total)*100}

    return dic

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

def build_degree_json(df):
    def merge_dicts(dict1, dict2, dict3):
        dict_out = {}
        for key, value in dict1.items():
            v2 = dict2[key] if key in dict2 else None
            v3 = dict3[key] if key in dict3 else None
            dict_out[key] = {'ira_medio': value, 'sem_evasao': v2, 'formatura': v3}
        return dict_out
    dic = merge_dicts(average_ira_graph(df),current_students_average_ira_graph(df),graduates_average_ira_graph(df))
    degree_json = {
        "ira_medio_grafico": json.dumps(sorted(dic.items())),
        "evasao_grafico": json.dumps(sorted(period_evasion_graph(df).items())),
        "ira_atual": current_students_ira(df),
        "ira_medio": general_ira(df),
        "qtd_alunos": total_students(df),
        "qtd_alunos_atuais": current_total_students(df),
        "taxa_evasao": general_evasion_rate(df),
        "taxa_formatura": average_graduation(df),
        "taxa_reprovacao": general_failure(df),
        "taxa_reprovacao_atual": current_students_failure(df),
        "tempo_formatura": average_graduation_time(df),
    }
    with open("cache/curso/curso.json",'w') as f:
        f.write(json.dumps(degree_json,indent=4))