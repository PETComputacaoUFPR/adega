import numpy as np
import math

from utils.situations import *
ANO_ATUAL = 2017
SEMESTRE_ATUAL = 2

# ++++++ Funcoes auxiliares +++++++

def weighted_avg_and_std(values, weights):
	average = np.average(values, weights=weights)
	# Fast and numerically precise:
	variance = np.average((values-average)**2, weights=weights)
	return math.sqrt(variance)

def listagem_turma_ingresso(df):
	# print(df.groupby(["ANO_INGRESSO", "SEMESTRE_INGRESSO"]).groups)
	grupos = df.groupby(["ANO_INGRESSO", "SEMESTRE_INGRESSO"]).groups
	for t in grupos:
		print(t)
		print("\n\n")
		print(df["FORMA_INGRESSO"][grupos[t]].drop_duplicates())

# +++++++++++++++++++++++++++++++++++

def calcular_ira_medio(df):
	ira_medio_turmaIngresso = {}
	grupos = df.loc[ df["SITUACAO"].isin(Situation.SITUATION_AFFECT_IRA) ].groupby(["ANO_INGRESSO", "SEMESTRE_INGRESSO"]).groups
	for t in grupos:
		#print(t)
		#print( df["NOME_PESSOA"][grupos[t]].drop_duplicates().count() );
		ira_medio_turmaIngresso[ t ] = np.average( df["MEDIA_FINAL"][ grupos[t] ], weights=df["TOTAL_CARGA_HORARIA"][ grupos[t] ] )
	
	print(ira_medio_turmaIngresso)
	return ira_medio_turmaIngresso

def calcular_ira_medio_desvio_padrao(df): 
	dp_turmaIngresso = {}
	grupos = df.loc[ df["SITUACAO"].isin(Situation.SITUATION_AFFECT_IRA) ].groupby(["ANO_INGRESSO", "SEMESTRE_INGRESSO"]).groups
	for t in grupos:
		dp_turmaIngresso[ t ] = weighted_avg_and_std( df["MEDIA_FINAL"][ grupos[t] ], weights=df["TOTAL_CARGA_HORARIA"][ grupos[t] ] );
	print(dp_turmaIngresso)
	return dp_turmaIngresso

def calcular_ira_semestre(df, ano, periodo):
	grupos = df.loc[ (df["SITUACAO"].isin(Situation.SITUATION_AFFECT_IRA))&(df["ANO"] == ano)&(df["PERIODO"] == periodo) ].groupby(["ANO_INGRESSO", "SEMESTRE_INGRESSO"]).groups
		
	print(grupos)
	#return ira_semestre


# NAO ENTENDI
def calcular_ira_semestre_desvio_padrao(media, turma_ingresso, ano, semestre, qtd_semestres):
	pass








