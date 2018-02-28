import re
import os
import sys
import pandas as pd
import numpy as np
from glob import glob
from json import load as json_load
from utils.situations import *



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
        #~ dh.students.aggregate(teste)
#       print(dh.students['MEDIA_FINAL'].aggregate(teste))
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
                if df['name'] == 'matricula.xls'  or df['name'] == 'matricula.csv':
                        register = df['dataframe']

        #~ clean_history(history)
        clean_register(register)
        #~ df.dropna(axis=0, how='all')
        history["MEDIA_FINAL"] = pd.to_numeric(history["MEDIA_FINAL"], errors='coerce')
        history = history[np.isfinite(history['MEDIA_FINAL'])]


        merged = pd.merge(history, register, how='outer', on=['MATR_ALUNO'])
        merged = merged.rename(index=str, columns={"ANO_INGRESSO_x": "ANO_INGRESSO", "SEMESTRE_INGRESSO_x": "SEMESTRE_INGRESSO", "FORMA_INGRESSO_x": "FORMA_INGRESSO"})

        fix_situation(merged)
        fix_admission(merged)
        fix_evasion(merged)
        fix_carga(merged)


        return merged


def clean_history(df):
    df.drop(['ID_NOTA', 'CONCEITO', 'ID_LOCAL_DISPENSA', 'SITUACAO_CURRICULO',
             'ID_CURSO_ALUNO', 'ID_VERSAO_CURSO', 'ID_CURRIC_ALUNO',
             'ID_ATIV_CURRIC', 'SITUACAO_ITEM', 'ID_ESTRUTURA_CUR', 'NUM_VERSAO'
            ], axis=1, inplace=True)
    df['PERIODO'] = df['PERIODO'].str.split('o').str[0]

def clean_register(df):
        df_split = df['PERIODO_INGRESSO'].str.split('/')
        df['ANO_INGRESSO'] = df_split.str[0]
        df['SEMESTRE_INGRESSO'] = df_split.str[1].str.split('o').str[0]
        df_split = df['PERIODO_EVASAO'].str.split('/')
        df['ANO_EVASAO'] = df_split.str[0]
        df['SEMESTRE_EVASAO'] = df_split.str[1].str.split('o').str[0]


        df.drop(['ID_PESSOA', 'NOME_PESSOA', 'DT_NASCIMENTO', 'NOME_UNIDADE','COD_CURSO', 'PERIODO_INGRESSO', 'PERIODO_EVASAO'],axis=1, inplace=True)


def fix_situation(df):
        for situation in Situation.SITUATIONS:
                df.loc[df.SITUACAO == situation[1], 'SITUACAO'] = situation[0]


def fix_admission(df):
        for adm in AdmissionType.ADMISSION_FORM:
                df.loc[df.FORMA_INGRESSO == adm[1], 'FORMA_INGRESSO'] = adm[0]


def fix_carga(df):
        df["CH_TOTAL"] = df["CH_TEORICA"]+df["CH_PRATICA"]

def fix_evasion(df):
        evasionForms = [x[1] for x in EvasionForm.EVASION_FORM]
        df.loc[~df.FORMA_EVASAO.isin(evasionForms), 'FORMA_EVASAO'] = 100
        for evasion in EvasionForm.EVASION_FORM:
                #~ df.loc[df.FORMA_EVASAO.str.contains(evasion[1]).fillna(1.0), 'FORMA_EVASAO'] = evasion[0]
                df.loc[df.FORMA_EVASAO == evasion[1], 'FORMA_EVASAO'] = evasion[0]

                #~ if(evasion[0] == 100):
                        #~ for x in df.FORMA_EVASAO.str.contains(evasion[1]).fillna(False):
                                #~ if(x != 0.0):
                                        #~ print(x)
        #~ print(df.FORMA_EVASAO.str.contains(evasion[1]).fillna(5))
        #~ print(df[['MATR_ALUNO','FORMA_EVASAO']])
