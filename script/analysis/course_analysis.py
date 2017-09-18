# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
df = pd.read_excel("../base/historico.xls")

# imprime completamente um dataframe
def print_analise(d):
	with pd.option_context('display.max_rows', None, 'display.max_columns', 27):
		print(d)

# calcula as taxas
def func(x,matr):
	c = matr[x['COD_ATIV_CURRIC']].values[0]
	return (x['counts'] / c)

#quantidade de matriculas
def qnt_matr(df):
	return df.groupby(['COD_ATIV_CURRIC']).size()


def analise(df):
	c = df.groupby(['COD_ATIV_CURRIC']).size()
	diciplinas = df.groupby(['COD_ATIV_CURRIC','SIGLA']).size().reset_index(name='counts')
	i=diciplinas.groupby(['COD_ATIV_CURRIC','SIGLA','counts']).apply(lambda x: func(x,matr)).reset_index(name='taxas gerais')
	print_analise(i)

matr = qnt_matr(df)
analise(df)




















#
##f = lambda x: x / c[x]
## p = df.groupby(['COD_ATIV_CURRIC','SIGLA']).size().apply(lambda x: (x /c['CI055'])*100)
#k = (df.sort(['ANO','PERIODO']))
##(p.apply(lambda x: print(p['COD_ATIV_CURRIC'])))
#
## # .size().reset_index(name = "count");
## # c = p.groupby(['count','SIGLA']).size()
## ''' percorre mais uma vez a serie para aplicar a funcao lambida, se a '''
##  c = lambda x: x+1
## curses = df['COD_ATIV_CURRIC'].drop_duplicates()
## 'MATR_ALUNO','
