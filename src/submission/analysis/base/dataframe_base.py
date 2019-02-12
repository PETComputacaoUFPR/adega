import os
import pandas as pd
import numpy as np
from submission.analysis.utils.situations import *
from submission.analysis.utils.utils import invert_dict


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
    dh = DataframeHolder(dataframe)
    return dataframe


def read_excel(path, planilha='Planilha1'):
    return pd.read_excel(path)

def read_csv(path):
    return pd.read_csv(path)

def fix_dataframes(dataframes):
    for df in dataframes:
        if df['name'] == 'historico.xls' or df['name'] == 'historico.csv':
            history = df['dataframe']
            history.rename(columns={'DESCR_SITUACAO': 'SITUACAO'}, inplace=True)
        if df['name'] == 'matricula.xls' or df['name'] == 'matricula.csv':
            register = df['dataframe']

    #~ clean_history(history)
    clean_register(register)
    #~ df.dropna(axis=0, how='all')
    history["MEDIA_FINAL"] = pd.to_numeric(history["MEDIA_FINAL"], errors='coerce')
    history = history[np.isfinite(history['MEDIA_FINAL'])]

    # inner = exste nos dois relatórios, é o que a gente quer
    # o que fazer com quem não está em um dos dois é um questão em aberto
    merged = pd.merge(history, register, how='inner', on=['MATR_ALUNO'])
    merged = merged.rename(index=str, columns={
        "ANO_INGRESSO_x": "ANO_INGRESSO",
        "SEMESTRE_INGRESSO_x": "SEMESTRE_INGRESSO",
        "FORMA_INGRESSO_x": "FORMA_INGRESSO"
        })

    fix_situation(merged)
    fix_admission(merged)
    fix_evasion(merged)
    fix_carga(merged)

    return merged


def clean_history(df):
    print(df.columns)

    drop_columns = ['ID_NOTA', 'CONCEITO', 'ID_LOCAL_DISPENSA', 'SITUACAO_CURRICULO',
                    'ID_CURSO_ALUNO', 'ID_VERSAO_CURSO', 'ID_CURRIC_ALUNO',
                    'ID_ATIV_CURRIC', 'SITUACAO_ITEM', 'ID_ESTRUTURA_CUR'
                    ]

    drop_columns = [x for x in drop_columns if x in df.columns]

    df.drop(drop_columns, axis=1, inplace=True)

    # df['PERIODO'] = df['PERIODO'].str.split('o').str[0]


def clean_register(df):
    df_split = df['PERIODO_INGRESSO'].str.split('/')
    df['ANO_INGRESSO'] = df_split.str[0]
    df['SEMESTRE_INGRESSO'] = df_split.str[1].str.split('o').str[0]
    df_split = df['PERIODO_EVASAO'].str.split('/')
    df['ANO_EVASAO'] = df_split.str[0]
    df['SEMESTRE_EVASAO'] = df_split.str[1].str.split('o').str[0]

    drop_columns = ['ID_PESSOA', 'NOME_PESSOA', 'DT_NASCIMENTO', 'NOME_UNIDADE', 'COD_CURSO',
                    'PERIODO_INGRESSO', 'PERIODO_EVASAO']

    drop_columns = [x for x in drop_columns if x in df.columns]

    df.drop(drop_columns, axis=1, inplace=True)


def get_situation(d, default):

    def getter(x):
        return invert_dict(d).get(x, default)
    return getter


def fix_situation(df):
    df.rename(columns={"SITUACAO": "SITUACAO2"}, inplace=True)

    df['SITUACAO'] = df.SITUACAO2.apply(get_situation(Situation.SITUATIONS, Situation.SIT_OUTROS))

    df.drop(['SITUACAO2'], axis=1, inplace=True)


def fix_admission(df):
    df.rename(columns={'FORMA_INGRESSO': 'FORMA_INGRESSO2'}, inplace=True)

    df['FORMA_INGRESSO'] = df.FORMA_INGRESSO2.apply(get_situation(AdmissionType.ADMISSION_FORM,
                                                                  AdmissionType.AT_OUTROS))

    df.drop(['FORMA_INGRESSO2'], axis=1, inplace=True)


def fix_carga(df):
    df["CH_TOTAL"] = df["CH_TEORICA"]+df["CH_PRATICA"]


def fix_evasion(df):
    df.rename(columns={'FORMA_EVASAO': 'FORMA_EVASAO2'}, inplace=True)

    df['FORMA_EVASAO'] = df.FORMA_EVASAO2.apply(get_situation(EvasionForm.EVASION_FORM,
                                                              EvasionForm.EF_OUTROS))

    df.drop(['FORMA_EVASAO2'], axis=1, inplace=True)
