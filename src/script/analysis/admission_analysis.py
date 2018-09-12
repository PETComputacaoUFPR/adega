import numpy as np

from script.utils.situations import *
from script.analysis.student_analysis import ira_alunos
from collections import defaultdict

import numpy as np

ANO_ATUAL = 2017
SEMESTRE_ATUAL = 2

def admission_class_ira_per_semester(df):

	"""
	Calculate the average IRA in every semester of the admission classes.

	This function group the dataframe by admission classes. 
	Then group each class by semesters. 
	And finally group each semester by student. 
	Calculate each student's IRA and then the average IRA for the class.

	Parameters
	----------
	df : DataFrame
	
	Returns
	-------
	dict of {list:dict}

			dict_admission={
			(admission_class1):{semester1:ira, semester2:ira, ...},
			(admission_class2):{semester1:ira, semester2:ira, ...},
			...
			}

	Examples
	--------
	{('2005', '1'): {(2012, '1o. Semestre'): 0.485, 
					 (2007, '1o. Semestre'): 0.6186531973412296, ...} ...}
	"""

	df = df[df['SITUACAO'].isin(Situation.SITUATION_AFFECT_IRA)]
	df = df[ df['TOTAL_CARGA_HORARIA'] != 0]
	admission_grouped = df.groupby(['ANO_INGRESSO_y','SEMESTRE_INGRESSO'])
	dict_admission = {}
	
	for admission in admission_grouped:
	#admission_grouped is a tuple of tuples, each tuple contains 0-tuple year/semester & 1-dataframe 
		dict_ira_semester = {}
		semester_grouped = admission[1].groupby(['ANO','PERIODO'])
		
		for semester in semester_grouped:
			student_grouped = semester[1].groupby('ID_ALUNO')
			ira_class = 0
			
			for student in student_grouped:
				#TODO: Verify if this can be calculated without groupby
				ira_individual =( (student[1].MEDIA_FINAL*student[1].TOTAL_CARGA_HORARIA).sum() )/(100*student[1].TOTAL_CARGA_HORARIA.sum())
				ira_class += ira_individual
			ira_class = ira_class / len(student_grouped)
			dict_ira_semester.update({semester[0]:ira_class})		
		dict_admission.update({admission[0]:dict_ira_semester})
	return dict_admission

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

def taxa_de_evasao(df):
    students = df.drop_duplicates()

    turmas_ingresso = students.groupby([
        "ANO_INGRESSO",
        "SEMESTRE_INGRESSO"]
    ).groups

    resultados = {}

    for ti in turmas_ingresso:
        students_ti = students.loc[(df.ANO_INGRESSO == ti[0]) & (df.SEMESTRE_INGRESSO == ti[1])]
        ti_num_students = students_ti.shape[0]
        ti_num_evasions = students_ti.loc[(students_ti.FORMA_EVASAO != EvasionForm.EF_ATIVO) & (students_ti.FORMA_EVASAO != EvasionForm.EF_FORMATURA) & (students_ti.FORMA_EVASAO != EvasionForm.EF_REINTEGRACAO)].shape[0]
        
        resultados[ti] = ti_num_evasions/ti_num_students

    return resultados