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
	#~ lines = (df[["MATR_ALUNO","ANO","COD_ATIV_CURRIC","NOME_ATIV_CURRIC","MEDIA_FINAL","PERIODO","SITUACAO"]])
	#~ for st in (df.groupby("MATR_ALUNO")):
		#~ print(st[1]["MATR_ALUNO"])
		#~ print(st[1]["ANO"])
		#~ print(st[1]["COD_ATIV_CURRIC"])
		#~ print(st[1]["NOME_ATIV_CURRIC"])
		#~ print(st[1]["MEDIA_FINAL"])
		#~ print(st[1]["PERIODO"])
		#~ print(st[1]["SITUACAO"])
		#~ print("")
	#~ total_student = df['MATR_ALUNO'].drop_duplicates()
	#~ for st in total_student:
		#~ students[st] = []
		#~ hist = df[df["MATR_ALUNO"]==st]
		#~ for matr in hist:
			#~ print(hist["ANO"])
			#~ print(hist[matr]["COD_ATIV_CURRIC"])
			#~ print(hist[matr]["NOME_ATIV_CURRIC"])
			#~ print(hist[matr]["MEDIA_FINAL"])
			#~ print(hist[matr]["PERIODO"])
			#~ print(hist[matr]["SITUACAO"])
			#~ print(hist[matr])
			#~ print("")
