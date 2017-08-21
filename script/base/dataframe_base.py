import re
import os
import sys
import pandas as pd

from glob import glob
from json import load as json_load
from utils.situations import *


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
        if df['name'] == 'historico.xls':
            history = df['dataframe']
        if df['name'] == 'matricula.xls':
            register = df['dataframe']

    clean_history(history)
    clean_register(register)

    merged = pd.merge(history, register, how='right', on=['MATR_ALUNO'])

    fix_situation(merged)
#    fix_admission(merged)
    fix_evasion(merged)

    return merged


def clean_history(df):
    df.drop(['ID_NOTA', 'CONCEITO', 'ID_LOCAL_DISPENSA', 'SITUACAO_CURRICULO',
             'ID_CURSO_ALUNO', 'ID_VERSAO_CURSO', 'ID_CURRIC_ALUNO',
             'ID_ATIV_CURRIC', 'SITUACAO_ITEM', 'ID_ESTRUTURA_CUR'
            ], axis=1, inplace=True)
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
            ],axis=1, inplace=True)


def fix_situation(df):
    for situation in Situation.SITUATIONS:
        df.loc[df.SITUACAO == situation[1], 'SITUACAO'] = situation[0]


def fix_admission(df):
    for adm in AdmissionType.ADMISSION_FORM:
        df.loc[df.FORMA_INGRESSO == adm[1], 'FORMA_INGRESSO'] = adm[0]


def fix_evasion(df):
    for evasion in EvasionForm.EVASION_FORM:
        df.loc[df.FORMA_EVASAO.str.contains(evasion[1]).fillna(False), 'FORMA_EVASAO'] = evasion[0]