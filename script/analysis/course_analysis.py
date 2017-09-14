# -*- coding: utf-8 -*-

import pandas as pd 
import numpy as np

def print_analise(d):
	with pd.option_context('display.max_rows', None, 'display.max_columns', 27):
		print(d)
def analise(df):
	c = df.groupby(['COD_ATIV_CURRIC']).size()
	diciplinas = df.groupby(['COD_ATIV_CURRIC','SIGLA']).size().reset_index(name='counts')
	i=diciplinas.groupby(['COD_ATIV_CURRIC','SIGLA']).apply(lambda x: x['counts'] / (c[x['COD_ATIV_CURRIC']].values[0])).reset_index(name='taxas')
	print_analise(i)
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
#p
#df = pd.read_excel("../base/historico.xls")
