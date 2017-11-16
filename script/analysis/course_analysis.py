# -*- coding: utf-8 -*-
import pandas as pd
import json
import numpy as np
from utils.situations import *
def print_analise(d):
    '''imprime todo o dataframe, por default o pandas so imprime as
    10 linhas inicias a 10 finais, com essa funcao o pandas imprime
    as linhas '''
    with pd.option_context('display.max_rows', None, 'display.max_columns', 27):
        print(d)

# calcula as taxas
def func(x, matr):
    ''' esta funcao recebe como parametro uma linha do dataframe e a
quantidade de matriculas '''
    c = matr[x['COD_ATIV_CURRIC']].values[0]
    return (x['Quantidade'] / c)

# quantidade de matriculas
def counts_matr(df):
    return df.groupby(['COD_ATIV_CURRIC']).size()

# taxas e quantidades semetrais
def analysis(df):
    qnt_matr = counts_matr(df)  # quantidade de matriculas disciplina
    ''' conta quantas vezes os valores de 'SITUACAO' se repete para
    cada disciplina'''
    disciplinas = df.groupby(['COD_ATIV_CURRIC', 'SITUACAO']
                             ).size().reset_index(name='Quantidade')
    ''' adiciona mais uma coluna ao df disciplina com as taxas de cada valor
     de 'SITUACAO' '''
    disciplina = disciplinas.groupby(['COD_ATIV_CURRIC', 'SITUACAO', 'Quantidade']).apply(
        lambda x: func(x, qnt_matr)).reset_index(name='Taxas gerais')
    disciplina = disciplina.drop('level_3',1) # retira coluna duplicada do index
    # codigo que transforma o dataframe em um dicionario
    dict_disciplina = {}
    for dis in qnt_matr.keys():
         # separa o dataframe em disciplina
        disc = disciplina.loc[disciplina['COD_ATIV_CURRIC']==dis]
        disc = disc.drop('COD_ATIV_CURRIC',1) # elimina a coluna codigo
        # seta a coluna SITUACAO como index
        disc = disc.set_index('SITUACAO').to_dict()
        # para caso uma discipl. nao tenha um campo, coloca o campo com valor 0
        for i in Situation.SITUATIONS:
            if not(i[0] in disc['Quantidade'].keys()):
                disc['Quantidade'][i[0]] = 0
                disc['Taxas gerais'][i[0]] = 0
        dict_disciplina[dis] = disc
    return dict_disciplina

# quantidade de vezes cursadas ate obter a aprovacao
def qnt_aprov(df):
    qnt = df.groupby(['MATR_ALUNO', 'COD_ATIV_CURRIC']
                     ).size().reset_index(name='qnt_aprov')
    return qnt
# transforma o dataframe geral em json, # TODO: fazer o mesmo com o semestral
def df_to_json(disciplina,qnt_matr):
        # cria o json
        with open(dis+'.json','w') as f:
            json.dump(disc,f,indent=4)

def matr_semestre(df):
    return df.groupby(['COD_ATIV_CURRIC', 'PERIODO', 'ANO']).size()


def func_semestre(x, matr):
    # print (matr)
    ano = int(x['ANO'])
    # print(ano)
    periodo = x['PERIODO'].values[0]
    disciplina = x['COD_ATIV_CURRIC'].values[0]
    c = matr[disciplina,periodo,ano]
    return (x['counts_semestre'] / c)


def analysis_semestre(df):
    qnt_matr_semestre = matr_semestre(df)
    discipline_semestre = df.groupby(['COD_ATIV_CURRIC', 'PERIODO', 'ANO', 'SITUACAO'])
    discipline_semestre = discipline_semestre.size()

    discipline_semestre = discipline_semestre.reset_index(name='counts_semestre')

    discipline_semestre = discipline_semestre.groupby(['COD_ATIV_CURRIC', 'PERIODO', 'ANO', 'SITUACAO'])

    discipline_semestre = discipline_semestre.apply(lambda x: func_semestre(x, qnt_matr_semestre))

    discipline_semestre = discipline_semestre.reset_index(name='taxas_semetrais')
    for dis in qnt_matr_semestre.keys():
        dis = ['CI055']
        disc = discipline_semestre.loc[discipline_semestre['COD_ATIV_CURRIC']==dis[0]].drop('COD_ATIV_CURRIC',1) # elimina a coluna codigo
        disc = disc.drop('level_4',1)
        print(dis[0])
        print(disc.set_index('ANO'))
        # seta a coluna SITUACAO como index
        disc = disc.set_index('ANO').to_dict('index')
        # with open(dis+'.json','w') as f:
            # json.dump(disc,f,indent=4)
        print("--------------------------------------------------------------------------------")

        break
    return discipline_semestre



def Main(df):

    # Analysis = analysis(df)
    Analysis_semestre = analysis_semestre(df)
    # matr = counts_matr(df)
    # df_to_json(Analysis,matr)
    # matr_semes = matr_semestre(df)
    # print_analise(matr_semes)
