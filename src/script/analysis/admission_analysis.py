import numpy as np

from script.utils.situations import *
from script.analysis.student_analysis import ira_alunos
from collections import defaultdict

import numpy as np

ANO_ATUAL = 2017
SEMESTRE_ATUAL = 2

def iras_alunos_turmas_ingressos(df):
	iras = ira_alunos(df)
	
	turmas_ingresso_grr = df.groupby([
		"ANO_INGRESSO",
		"SEMESTRE_INGRESSO",
		"MATR_ALUNO"]
	).groups
	
	# Cria um dicionario cujas chaves são GRR
	# e valor são tuplas (ano_ingresso,semestre_ingresso)
	ano_semestre_do_grr = {}
	for ti in turmas_ingresso_grr:
		ano_semestre_do_grr[ ti[2] ] = (ti[0],ti[1])
	
	resultados = defaultdict(list)
	

	for grr in iras:
		semestre_ano = ano_semestre_do_grr[grr]
		resultados[ semestre_ano ].append(iras[grr])

	return resultados



def media_ira_turma_ingresso(df):
	iras_alunos_por_turma = iras_alunos_turmas_ingressos(df)
	# Calcula a média do ira para cada turma_ingresso
	resultados = {}
	for r in iras_alunos_por_turma:
		aux = np.array(iras_alunos_por_turma[r])
		resultados[r] = np.mean(aux)
	
	return resultados

def desvio_padrao_turma_ingresso(df):
	iras_alunos_por_turma = iras_alunos_turmas_ingressos(df)
	# Calcula o desvio padrão para cada turma_ingresso
	resultados = {}
	for r in iras_alunos_por_turma:
		aux = np.array(iras_alunos_por_turma[r])
		resultados[r] = np.std(aux)
	
	return resultados
