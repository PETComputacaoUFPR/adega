
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

def fix_dataframes(dataframes):
        for df in dataframes:
                if df['name'] == 'historico.xls' or df['name'] == 'historico.csv':
                        history = df['dataframe']
                        history.rename(columns={'DESCR_SITUACAO': 'SITUACAO'}, inplace=True)
                if df['name'] == 'matricula.xls'  or df['name'] == 'matricula.csv':
                        register = df['dataframe']
                if df['name'] == 'disciplinas.xls' or df['name'] == 'disciplinas.csv':
                    disciplinas = df['dataframe'] 
                    disciplinas.rename(columns={'COD_DISCIPLINA': 'COD_ATIV_CURRIC'}, inplace=True)

        clean_history(history)
        clean_register(register)

        #adiciona disciplinas do primeiro periodo de BCC
        disciplinas = pd.merge(disciplinas, disciplinas_pp(disciplinas), how='outer', on=['COD_ATIV_CURRIC'], suffixes=('', '_y'))
        fix_disciplinas(disciplinas)
        #end
        disciplinas = disciplinas.drop_duplicates('COD_ATIV_CURRIC')
        clean_disciplinas(disciplinas)
        disciplinas = disciplinas.sort_values(by=['COD_ATIV_CURRIC'])

        #~ df.dropna(axis=0, how='all')
        history["MEDIA_FINAL"] = pd.to_numeric(history["MEDIA_FINAL"], errors='coerce')
        history = history[np.isfinite(history['MEDIA_FINAL'])]
        fix_register(register) 

        merged = pd.merge(history, register, how='outer', on=['MATR_ALUNO'], suffixes=('', '_y'))
        merged = pd.merge(merged, disciplinas, how='left', on=['COD_ATIV_CURRIC'])

        drop_y(merged)

        fix_situation(merged)
        fix_admission(merged)
        fix_evasion(merged)
        fix_carga(merged)

        #adiciona disciplinas optativas desse ano, coloca -1 em "nao materias"
        grade_atual = int(merged['NUM_VERSAO'].max())
        merged.ix[merged['CREDITOS'] == 0, 'PERIODO_IDEAL'] = merged.ix[merged['CREDITOS'] == 0, 'PERIODO_IDEAL'].fillna(-1)
        merged.ix[merged['NUM_VERSAO'] == (grade_atual), 'PERIODO_IDEAL'] = merged.ix[merged['NUM_VERSAO'] == (grade_atual), 'PERIODO_IDEAL'].fillna(0)
        #end

        return merged


def clean_disciplinas(df):
    df.drop(['COD_CURSO', 'NOME_UNIDADE', 'NUM_VERSAO', 'NOME_DISCIPLINA',
        'COD_PRE_REQ', 'NOME_PRE_REQ', 'TIPO_REQUISITO', 'NUM_REFERENCIA',
        'ITEM_TABELA', 'ID_ESTRUTURA_CUR'], axis=1, inplace=True)

def clean_history(df):
    # df.drop(['ID_NOTA', 'CONCEITO', 'ID_LOCAL_DISPENSA', 'SITUACAO_CURRICULO',
    #          'ID_CURSO_ALUNO', 'ID_VERSAO_CURSO', 'ID_CURRIC_ALUNO',
    #          'ID_ATIV_CURRIC', 'SITUACAO_ITEM', 'ID_ESTRUTURA_CUR', 'NUM_VERSAO'
    #         ], axis=1, inplace=True) comentei porque clean_history estava comentado por algum motivo(perguntar)
    df['PERIODO'] = df['PERIODO'].str.split('o').str[0]
def normaliza_semestre(x):
    if pd.isnull(x):
        return 0
    return 2 if (int(x) > 6 ) else 1  
def fix_register(df):
    df.rename(columns={'MATRICULA': 'MATR_ALUNO'}, inplace=True)
def clean_register(df):
        df_split = df['DT_INGRESSO'].str.split('/')  
        #df_split = df['PERIODO_INGRESSO'].str.split('/')
        df['ANO_INGRESSO'] = df_split.str[2]
        df['SEMESTRE_INGRESSO'] = df_split.str[1].apply(lambda x: normaliza_semestre(x) )  

        df_split = df['PERIODO_EVASAO'].str.split(' ')
        df['ANO_EVASAO'] = df_split.str[0]
        df['SEMESTRE_EVASAO'] = df_split.str[1].str.split('o').str[0]


        df.drop(['COD_CURSO','PERIODO_EVASAO'],axis=1, inplace=True)


def fix_situation(df):
        for situation in Situation.SITUATIONS:
               # print(situation) 
               # print(df.loc[df.SITUACAO==situation[1]] ) 
               # print("----------------------------------------------" ) 
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

def fix_disciplinas(df):
    drop_y(df)
    df['PERIODO_IDEAL'] = df['PERIODO_IDEAL'].fillna(1)
    df['DESCR_ESTRUTURA'] = df['DESCR_ESTRUTURA'].fillna("Obrigatórias")

def disciplinas_pp(df):
    disc_pp = df.copy()
    disc_pp = disc_pp[(disc_pp.PERIODO_IDEAL == 2) | (disc_pp.PERIODO_IDEAL == 3)]
    disc_pp = fix_disc_pp(disc_pp)
    disc_pp = disc_pp.drop_duplicates('COD_ATIV_CURRIC')
    disc_pp = pd.merge(disc_pp, df, on=['COD_ATIV_CURRIC'], how='left', suffixes=('_y', ''))
    drop_y(disc_pp)
    return disc_pp

def fix_disc_pp(df):
    df.rename(columns={'COD_ATIV_CURRIC': 'COD_DISCIPLINA'}, inplace=True)
    df.rename(columns={'COD_PRE_REQ': 'COD_ATIV_CURRIC'}, inplace=True)
    df.rename(columns={'COD_DISCIPLINA': 'COD_PRE_REQ'}, inplace=True)
    return df

def drop_y(df):
    to_drop = [y for y in df if y.endswith('_y')]
    df.drop(to_drop, axis=1, inplace=True)
