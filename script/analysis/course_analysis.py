# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
df = pd.read_excel("../base/base-2016-1/historico.xls")

# imprime completamente um dataframe
def print_analise(d):
	with pd.option_context('display.max_rows', None, 'display.max_columns', 27):
		print(d)

# calcula as taxas
def func(x,matr):
	c = matr[x['COD_ATIV_CURRIC']].values[0]
	return (x['counts'] / c)

#quantidade de matriculas
def counts_matr(df):
	return df.groupby(['COD_ATIV_CURRIC']).size()


def analysis(df):
	qnt_matr = counts_matr(df) #quantidade de matriculas disciplina
	#conta quantas vezes os valores de 'SIGLA' se repete para cada disciplina
	disciplinas = df.groupby(['COD_ATIV_CURRIC','SIGLA']).size().reset_index(name='counts')
	#adiciona mais uma coluna ao df disciplina com as taxas de cada valor de 'SIGLA'
	disciplina=disciplinas.groupby(['COD_ATIV_CURRIC','SIGLA','counts']).apply(lambda x: func(x,matr)).reset_index(name='taxas gerais')
	return disciplina
