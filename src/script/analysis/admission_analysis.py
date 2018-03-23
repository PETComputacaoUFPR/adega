import numpy as np

from script.utils.situations import *
ANO_ATUAL = 2017
SEMESTRE_ATUAL = 2


def listagem_turma_ingresso(df):
	#~ print(df.groupby(["ANO_INGRESSO", "SEMESTRE_INGRESSO"]).groups)
	grupos = df.groupby(["ANO_INGRESSO", "SEMESTRE_INGRESSO"]).groups
	for t in grupos:
		print(t)
		print("\n\n")
		print(df["FORMA_INGRESSO"][grupos[t]].drop_duplicates())
