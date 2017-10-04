import pandas as pd
from utils.situations import *

def average_ira(d):
    temp = d.dropna(subset=['MEDIA_FINAL'])
    temp = temp[temp['MEDIA_FINAL'] <= 100]
    if not temp.empty:
        #print(temp[['MEDIA_FINAL', 'CH_TOTAL']])
        aux = np.sum(temp['MEDIA_FINAL']*temp['CH_TOTAL'])
        ch_total = np.sum(temp['CH_TOTAL']) * 100
        print(aux/ch_total)

def indice_aprovacao_semestral(df):
	students = {}
	df = df.dropna(subset=['MEDIA_FINAL'])
	total_students = len(df["MATR_ALUNO"])
	for i in range(total_students):
		matr = (df["MATR_ALUNO"][i])
		if(not (matr in students)):
			students[matr] = {}
		
		
		ano = str(df["ANO"][i])
		semestre = str(df["PERIODO"][i])
		situacao = int(df["SITUACAO"][i])
		
		
		if not(ano+"/"+semestre in students[matr]):
			students[matr][ano+"/"+semestre] = [0,0]
		
		if(situacao in Situation.SITUATION_PASS):
			students[matr][ano+"/"+semestre][0]+=1
			students[matr][ano+"/"+semestre][1]+=1
		if(situacao in Situation.SITUATION_FAIL):
			students[matr][ano+"/"+semestre][1]+=1
	print(students)
		

def aluno_turmas(df):
	students = {}
	df = df.dropna(subset=['MEDIA_FINAL'])
	total_students = len(df["MATR_ALUNO"])
	for i in range(total_students):
		matr = (df["MATR_ALUNO"][i])
		if(not (matr in students)):
			students[matr] = []
		
		for s in Situation.SITUATIONS:
			if(s[0] == df["SITUACAO"][i]):
				situacao = s[1]
				break
		ano = (df["ANO"][i])
		codigo = (df["COD_ATIV_CURRIC"][i])
		nome = (df["NOME_ATIV_CURRIC"][i])
		nota = (df["MEDIA_FINAL"][i])
		semestre = (df["PERIODO"][i])
		
		students[matr].append({
			"ano": ano,
			"codigo": codigo,
			"nome": nome,
			"nota": nota,
			"semestre": semestre,
			"situacao": situacao
		})
	print(students)
