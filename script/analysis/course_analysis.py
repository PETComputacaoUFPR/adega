# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import utils.situations
df = pd.read_excel("../base/base-2016-1/historico.xls")

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
        lambda x: func(x, matr)).reset_index(name='taxas gerais')
    return disciplina
# quantidade de vezes cursadas ate obter a aprovacao


def qnt_aprov(df):
    qnt = df.groupby(['MATR_ALUNO','COD_ATIV_CURRIC']).size().reset_index(name='quantida aprov')
    return qnt
    # print(qnt)


matr = counts_matr(df)
analysis(df)
qnt_aprov(df)

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
