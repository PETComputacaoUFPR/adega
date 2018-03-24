
import os
import pandas as pd
import numpy as np
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

def printdf(df):
    for index, row in df.iterrows():
        print(index)
        print(row)
    print('end')

def fix_dataframes(dataframes):
        for df in dataframes:
                if df['name'] == 'historico.xls' or df['name'] == 'historico.csv':
                        history = df['dataframe']
                        history.rename(columns={'DESCR_SITUACAO': 'SITUACAO'}, inplace=True)
                if df['name'] == 'matricula.xls'  or df['name'] == 'matricula.csv':
                        register = df['dataframe']
                if df['name'] == 'disciplinas.xls' or df['name'] == 'disciplinas.csv':
                    disciplina = df['dataframe'] 
                    disciplina.rename(columns={'COD_DISCIPLINA': 'COD_ATIV_CURRIC'}, inplace=True)

        clean_history(history)
        clean_register(register)

        #adiciona disciplinas do primeiro periodo de BCC
        disc_b = disciplina.copy()
        disciplina_pp = disciplina.copy()
        disciplina_pp = disciplina_pp[(disciplina_pp.PERIODO_IDEAL == 2) | (disciplina_pp.PERIODO_IDEAL == 3)]
        disciplina_pp = fix_disciplina_pp(disciplina_pp)
        disciplina_pp = disciplina_pp.drop_duplicates('COD_ATIV_CURRIC')
        disciplina_pp = pd.merge(disciplina_pp, disciplina, on=['COD_ATIV_CURRIC'], how='left', suffixes=('_y', ''))
        drop_y(disciplina_pp)
        disciplina = pd.merge(disciplina, disciplina_pp, how='outer', on=['COD_ATIV_CURRIC'], suffixes=('', '_y'))
        drop_y(disciplina)
        disciplina['PERIODO_IDEAL'] = disciplina['PERIODO_IDEAL'].fillna(1)
        disciplina['DESCR_ESTRUTURA'] = disciplina['DESCR_ESTRUTURA'].fillna("Obrigatórias")
        #end

        disciplina = disciplina.drop_duplicates('COD_ATIV_CURRIC')
        clean_disciplina(disciplina)
        
        disciplina = disciplina.sort_values(by=['COD_ATIV_CURRIC'])

        #~ df.dropna(axis=0, how='all')
        history["MEDIA_FINAL"] = pd.to_numeric(history["MEDIA_FINAL"], errors='coerce')
        history = history[np.isfinite(history['MEDIA_FINAL'])]

        merged = pd.merge(history, register, how='outer', on=['MATR_ALUNO'], suffixes=('', '_y'))
        merged = pd.merge(merged, disciplina, how='left', on=['COD_ATIV_CURRIC'])

        drop_y(merged)

        fix_situation(merged)
        fix_admission(merged)
        fix_evasion(merged)
        fix_carga(merged)


        return merged


def clean_disciplina(df):
    df.drop(['COD_CURSO', 'NOME_UNIDADE', 'NUM_VERSAO', 'NOME_DISCIPLINA',
        'COD_PRE_REQ', 'NOME_PRE_REQ', 'TIPO_REQUISITO', 'NUM_REFERENCIA',
        'ITEM_TABELA', 'ID_ESTRUTURA_CUR'], axis=1, inplace=True)

def clean_history(df):
    # df.drop(['ID_NOTA', 'CONCEITO', 'ID_LOCAL_DISPENSA', 'SITUACAO_CURRICULO',
    #          'ID_CURSO_ALUNO', 'ID_VERSAO_CURSO', 'ID_CURRIC_ALUNO',
    #          'ID_ATIV_CURRIC', 'SITUACAO_ITEM', 'ID_ESTRUTURA_CUR', 'NUM_VERSAO'
    #         ], axis=1, inplace=True) comentei porque clean_history estava comentado por algum motivo(perguntar)
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
        
def fix_disciplina_pp(df):
    copy = df
    copy.rename(columns={'COD_ATIV_CURRIC': 'COD_DISCIPLINA'}, inplace=True)
    copy.rename(columns={'COD_PRE_REQ': 'COD_ATIV_CURRIC'}, inplace=True)
    copy.rename(columns={'COD_DISCIPLINA': 'COD_PRE_REQ'}, inplace=True)
    return copy

def drop_y(df):
    to_drop = [y for y in df if y.endswith('_y')]
    df.drop(to_drop, axis=1, inplace=True)
