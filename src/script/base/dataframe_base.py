import os
import pandas as pd
import numpy as np
from script.utils.situations import *


class DataframeHolder:
    def __init__(self, dataframe):
        self.students = dataframe.groupby('MATR_ALUNO')
        self.courses = dataframe.groupby('COD_ATIV_CURRIC')
        self.admission = dataframe.groupby(['ANO_INGRESSO', 'SEMESTRE_INGRESSO'])


def load_dataframes(cwd='.'):
    dataframes = []
    for path, dirs, files in os.walk(cwd):
        for f in files:
            file_path = path + '/' + f
            dh = {'name': f, 'dataframe': None}
            if 'csv' in f:
                dh['dataframe'] = read_csv(file_path)
            if 'xls' in f:
                dh['dataframe'] = read_excel(file_path)

            if dh['dataframe'] is not None:
                dataframes.append(dh)

    dataframe = fix_dataframes(dataframes)

    return dataframe


def read_excel(path, planilha='Planilha1'):
    return pd.read_excel(path)


def read_csv(path):
    return pd.read_csv(path)


def fix_dataframes(dataframes):
    for df in dataframes:
        if df['name'] == 'historico.xls' or df['name'] == 'historico.csv':
            history = df['dataframe']
        if df['name'] == 'matricula.xls' or df['name'] == 'matricula.csv':
            register = df['dataframe']

    clean_history(history)
    clean_register(register)
    # ~ df.dropna(axis=0, how='all')
    history["MEDIA_FINAL"] = pd.to_numeric(history["MEDIA_FINAL"], errors='coerce')
    history = history[np.isfinite(history['MEDIA_FINAL'])]

    # FIXME: how='inner' só aceita caras que estejam nos dois relatórios
    merged = pd.merge(history, register, how='right', on=['MATR_ALUNO'])
    # ~ print(merged)
    fix_situation(merged)
    #	fix_admission(merged)
    fix_evasion(merged)

    return merged


def clean_history(df):
    print(df.columns)

    drop_columns = ['ID_NOTA', 'CONCEITO', 'ID_LOCAL_DISPENSA', 'SITUACAO_CURRICULO',
        'ID_CURSO_ALUNO', 'ID_VERSAO_CURSO', 'ID_CURRIC_ALUNO',
        'ID_ATIV_CURRIC', 'SITUACAO_ITEM', 'ID_ESTRUTURA_CUR'
    ]

    drop_columns = [x for x in drop_columns if x in df.columns]

    df.drop(drop_columns, axis=1, inplace=True)
    df['PERIODO'] = df['PERIODO'].str.split('o').str[0]


def clean_register(df):
    df_split = df['PERIODO_INGRESSO'].str.split('/')
    df['ANO_INGRESSO'] = df_split.str[0]
    df['SEMESTRE_INGRESSO'] = df_split.str[1].str.split('o').str[0]
    df_split = df['PERIODO_EVASAO'].str.split('/')
    df['ANO_EVASAO'] = df_split.str[0]
    df['SEMESTRE_EVASAO'] = df_split.str[1].str.split('o').str[0]

    df.drop(['ID_PESSOA', 'NOME_PESSOA', 'DT_NASCIMENTO', 'NOME_UNIDADE',
             'COD_CURSO', 'NUM_VERSAO', 'PERIODO_INGRESSO', 'PERIODO_EVASAO',
             ], axis=1, inplace=True)


def fix_situation(df):
    for situation in Situation.SITUATIONS:
        df.loc[df.SITUACAO == situation[1], 'SITUACAO'] = situation[0]


def fix_admission(df):
    for adm in AdmissionType.ADMISSION_FORM:
        df.loc[df.FORMA_INGRESSO == adm[1], 'FORMA_INGRESSO'] = adm[0]


def fix_evasion(df):
    evasionForms = [x[1] for x in EvasionForm.EVASION_FORM]
    df.loc[~df.FORMA_EVASAO.isin(evasionForms), 'FORMA_EVASAO'] = 100
    for evasion in EvasionForm.EVASION_FORM:
        # ~ df.loc[df.FORMA_EVASAO.str.contains(evasion[1]).fillna(1.0), 'FORMA_EVASAO'] = evasion[0]
        df.loc[df.FORMA_EVASAO == evasion[1], 'FORMA_EVASAO'] = evasion[0]

    # ~ if(evasion[0] == 100):
    # ~ for x in df.FORMA_EVASAO.str.contains(evasion[1]).fillna(False):
    # ~ if(x != 0.0):
    # ~ print(x)
# ~ print(df.FORMA_EVASAO.str.contains(evasion[1]).fillna(5))
# ~ print(df[['MATR_ALUNO','FORMA_EVASAO']])
