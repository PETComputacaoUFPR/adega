import pandas as pd
from utils.situations import *


ANO_ATUAL = 2018
SEMESTRE_ATUAL = 1

def average_ira(d):
    temp = d.dropna(subset=['MEDIA_FINAL'])
    temp = temp[temp['MEDIA_FINAL'] <= 100]
    if not temp.empty:
        #print(temp[['MEDIA_FINAL', 'CH_TOTAL']])
        aux = np.sum(temp['MEDIA_FINAL']*temp['CH_TOTAL'])
        ch_total = np.sum(temp['CH_TOTAL']) * 100
        return(aux/ch_total)

def periodo_pretendido(df):
	aux = df.groupby(["MATR_ALUNO","ANO_INGRESSO","SEMESTRE_INGRESSO"])
	students = {}
	for x in aux:
		print(x[0][0] + " : "+x[0][1]+" "+x[0][2]) 
		students[x[0][0]] = (ANO_ATUAL - int(x[0][1]))*2 + SEMESTRE_ATUAL - int(x[0][2]) + 1
	return students

def ira_semestra(df):
	aux = ira_por_quantidade_disciplinas(df)
	for matr in aux:
		for periodo in aux[matr]:
			aux[matr][periodo] = aux[matr][periodo][0]
	return aux

def ira_por_quantidade_disciplinas(df):
	students = {}
	df = df.dropna(subset=['MEDIA_FINAL'])
	total_students = len(df["MATR_ALUNO"])
	for i in range(total_students):
		matr = (df["MATR_ALUNO"][i])
		if(not (matr in students)):
			students[matr] = {}
		
		
		ano = str(int(df["ANO"][i]))
		semestre = str(df["PERIODO"][i])
		situacao = int(df["SITUACAO"][i])
		nota = float(df["MEDIA_FINAL"][i])
		
		
		
		
		if(situacao in Situation.SITUATION_AFFECT_IRA):
			if not(ano+"/"+semestre in students[matr]):
				students[matr][ano+"/"+semestre] = [0,0]
			students[matr][ano+"/"+semestre][0]+=nota
			students[matr][ano+"/"+semestre][1]+=1
	
	for matr in students:
		for periodo in students[matr]:
			if(students[matr][periodo][1] != 0):
				students[matr][periodo][0]/=students[matr][periodo][1]*100
	return(students)

def indice_aprovacao_semestral(df):
	students = {}
	df = df.dropna(subset=['MEDIA_FINAL'])
	total_students = len(df["MATR_ALUNO"])
	for i in range(total_students):
		matr = (df["MATR_ALUNO"][i])
		if(not (matr in students)):
			students[matr] = {}
		
		
		ano = str(int(df["ANO"][i]))
		semestre = str(df["PERIODO"][i])
		situacao = int(df["SITUACAO"][i])
		
		
		if not(ano+"/"+semestre in students[matr]):
			students[matr][ano+"/"+semestre] = [0,0]
		
		if(situacao in Situation.SITUATION_PASS):
			students[matr][ano+"/"+semestre][0]+=1
			students[matr][ano+"/"+semestre][1]+=1
		if(situacao in Situation.SITUATION_FAIL):
			students[matr][ano+"/"+semestre][1]+=1
	return(students)
		

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
		ano = str(int(df["ANO"][i]))
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
	return(students)
