# -*- coding: utf-8 -*-
import pandas as pd
import json
import numpy as np
import utils.situations

# df = pd.read_excel("../base/base-2016-1/historico.xls")
# imprime completamente um dataframe


def print_analise(d):
    with pd.option_context('display.max_rows', None, 'display.max_columns', 27):
        print(d)

# calcula as taxas


def func(x, matr):
    c = matr[x['COD_ATIV_CURRIC']].values[0]
    return (x['counts'] / c)

# quantidade de matriculas


def counts_matr(df):
    return df.groupby(['COD_ATIV_CURRIC']).size()


def analysis(df):
    qnt_matr = counts_matr(df)  # quantidade de matriculas disciplina
    # conta quantas vezes os valores de 'SIGLA' se repete para cada disciplina
    disciplinas = df.groupby(['COD_ATIV_CURRIC', 'SIGLA']
                             ).size().reset_index(name='counts')
    # adiciona mais uma coluna ao df disciplina com as taxas de cada valor de 'SIGLA'
    disciplina = disciplinas.groupby(['COD_ATIV_CURRIC', 'SIGLA', 'counts']).apply(
        lambda x: func(x, qnt_matr)).reset_index(name='taxas gerais')
    # print(disciplina)
    return disciplina
# quantidade de vezes cursadas ate obter a aprovacao


def qnt_aprov(df):
    qnt = df.groupby(['MATR_ALUNO', 'COD_ATIV_CURRIC']
                     ).size().reset_index(name='qnt_aprov')
    return qnt
    # print(qnt)


def matr_semestre(df):
    return df.groupby(['COD_ATIV_CURRIC', 'PERIODO', 'ANO']).size()


def func_semestre(x, matr):
    # print (matr)
    ano = int(x['ANO'])
    # print(ano)
    periodo = x['PERIODO'].values[0]
    disciplina = x['COD_ATIV_CURRIC'].values[0]
    c = matr[disciplina,periodo,ano]
    # break
    # print(x['PERIODO'])
    # print("Disciplina: %s\nPeriodo:%s \nAno:%d"%(disciplina,periodo,ano))
    # c = matr['CI056','2']
    # print(c)
    # print(disciplina)
    # print("--------------------------------------------------------------------------")
    return (x['counts_semestre'] / c)


def analysis_semestre(df):
    qnt_matr_semestre = matr_semestre(df)
    discipline_semestre = df.groupby(['COD_ATIV_CURRIC', 'PERIODO', 'ANO', 'SIGLA']).size(
    ).reset_index(name='counts_semestre')
    discipline_semestre = discipline_semestre.groupby(['COD_ATIV_CURRIC', 'PERIODO', 'ANO', 'SIGLA']).apply(lambda x: func_semestre(x,
                                                                                                        qnt_matr_semestre)).reset_index(name='taxas_semetrais')

    return discipline_semestre
def Main(df):
    Analysis = analysis(df)
    Analysis_semestre = analysis_semestre(df)
    matr = counts_matr(df)
    matr_semes = matr_semestre(df)
    print_analise(merged)
    
# main()
# matr = counts_matr(df)
# analysis(df)
# qnt_aprov(df)

#
##f = lambda x: x / c[x]
## p = df.groupby(['COD_ATIV_CURRIC','SIGLA']).size().apply(lambda x: (x /c['CI055'])*100)
#k = (df.sort(['ANO','PERIODO']))
##(p.apply(lambda x: print(p['COD_ATIV_CURRIC'])))
#
# .size().reset_index(name = "count");
# c = p.groupby(['count','SIGLA']).size()
## ''' percorre mais uma vez a serie para aplicar a funcao lambida, se a '''
##  c = lambda x: x+1
## curses = df['COD_ATIV_CURRIC'].drop_duplicates()
# 'MATR_ALUNO','
