# -*- coding: utf-8 -*-
from datetime import datetime
import pprint
import pandas as pd
import json
import numpy as np
from script.utils.situations import Situation as sit
def grafico(df,lista_disciplinas): 
			for disciplina in lista_disciplinas.keys() :
				qtd_aluno = lista_disciplinas[disciplina]["qtd_alunos"] 
				dic = {"00-4.9":0.0 , "05-9.9":0.0 , "10-14.9":0.0 , "15-19.9":0.0 , "20-24.9":0.0 , "25-29.9":0.0 , "30-34.9":0.0 ,
					   "35-39.9":0.0 , "40-44.9":0.0 , "45-49.9":0.0 , "50-54.9":0.0 , "55-59.9":0.0 , "60-64.9":0.0 , "65-69.9":0.0 ,
					   "70-74.9":0.0 , "75-79.9":0.0 , "80-84.9":0.0 , "85-89.9":0.0 , "90-94.9":0.0 ,"95-100": 0.0}
				disciplina_df = df.loc[df.COD_ATIV_CURRIC == disciplina] 
				disci_lista = [] 
				for i in disciplina_df.iterrows():
					nota = 0.0 if i[1].MEDIA_FINAL > 100 else i[1].MEDIA_FINAL 
					for key in dic.keys():
						a = key.split('-') 
						value_min = float(a[0])  
						value_max = float(a[1])  
						if((nota >= value_min) and (nota <= value_max)): 
							dic[key] += float(nota)   
							break;
				for j in dic.keys():
					disci_lista.append([j, 0.0 if qtd_aluno == 0 else dic[j] / qtd_aluno])

				lista_disciplinas[disciplina]["compara_nota"]  = disci_lista




def informacoes_gerais(df,lista_disciplinas):
	#quantidade de matriculas
	disciplinas = df.groupby(["COD_ATIV_CURRIC"]).size()  
	for disciplina in disciplinas.index:
		disciplina_dict = {} 
		disciplina_df = df.loc[df.COD_ATIV_CURRIC == disciplina] 
		disciplina_dict["qtd_alunos"] = int(disciplinas[disciplina])   
		disciplina_dict["disciplina_codigo"] = disciplina 
		disciplina_dict["disciplina_nome"] = \
		disciplina_df.NOME_ATIV_CURRIC.values[0]	
		lista_disciplinas[disciplina] = disciplina_dict 
def conhecimento(qtd,disciplina_dict):
	conheci_df = qtd.loc[(qtd.SITUACAO == sit.SIT_CONHECIMENTO_APROVADO) |
			(qtd.SITUACAO == sit.SIT_CONHECIMENTO_REPROVADO)] 
	total_conheci = conheci_df.qtd.sum() 
	if np.isnan(total_conheci):
		total_conheci = 0
	conheci_aprov = conheci_df.loc[conheci_df.SITUACAO == \
			sit.SIT_CONHECIMENTO_APROVADO].set_index("COD_ATIV_CURRIC" ) 
	disciplina_dict["qtd_conhecimento"] = int(total_conheci)

	if (total_conheci !=0) and (not conheci_aprov.empty):
		disciplina_dict["taxa_conhecimento"] = float(conheci_aprov.qtd.values[0] /
				total_conheci)
	else:
		disciplina_dict["taxa_conhecimento"] = 0.0

def trancamento(qtd,disciplina_dict,qtd_matr):
	trancamento_df = qtd.loc[(qtd.SITUACAO == sit.SIT_TRANCAMENTO_ADMINISTRATIVO) | 
						(qtd.SITUACAO == sit.SIT_TRANCAMENTO_TOTAL) | 
						(qtd.SITUACAO == sit.SIT_CANCELADO)] 
	qtd_tranc = trancamento_df.qtd.sum() 
	if np.isnan(qtd_tranc):
		qtd_tranc = 0
	disciplina_dict["qtd_trancamento"] = int(qtd_tranc) 
	disciplina_dict["taxa_trancamento"] = float(qtd_tranc / qtd_matr) if qtd_matr else 0.0

 
def reprovacao(qtd,disciplina,qtd_matr,taxa_reprov_absoluta,taxa_reprov_freq): 
	"""existem as analises reprovacao absoluta, reprovacao por frequencia,	
	reprovacao absoluta, reprovacao por frequencia da ultima vez que a
	disciplina foi ofertada, a logica das analise sao a mesma so muda os valores
	do dataframe qtd e o nomes das chaves do dicionario,logo é possível reaproveitar
	o mesmo codigo para fazer analise geral e da ultima vez que foi ofertado.""" 
	sit_reprov = sit.SITUATION_FAIL + (sit.SIT_REPROVADO_SEM_NOTA,)
	reprov_df = qtd.loc[(qtd.SITUACAO == sit_reprov[0]) |
						(qtd.SITUACAO == sit_reprov[1]) |
						(qtd.SITUACAO == sit_reprov[2]) |
						(qtd.SITUACAO == sit_reprov[3]) ]
	qtd_reprov_abso = reprov_df.qtd.sum() #quantidade de reprovacao absoluta
	qtd_reprov_freq = reprov_df.loc[reprov_df.SITUACAO == sit_reprov[1]] 
	if qtd_matr != 0:
		if np.isnan(qtd_reprov_abso): 
			disciplina[taxa_reprov_absoluta] = 0.0
		else:
			disciplina[taxa_reprov_absoluta] = float(qtd_reprov_abso / qtd_matr)

		if qtd_reprov_freq.empty:
			disciplina[taxa_reprov_freq] = 0.0 
		else:
			disciplina[taxa_reprov_freq] = float(qtd_reprov_freq.qtd.values[0] / qtd_matr)

	else:
		disciplina[taxa_reprov_absoluta] = 0.0
		disciplina[taxa_reprov_freq] = 0.0 

def nota(notas_df,disciplina,index):
	notas = [] 
	for i in notas_df.iterrows():
		if i[1].SITUACAO in sit.SITUATION_AFFECT_IRA:
			nota = 0 if np.isnan(i[1].MEDIA_FINAL) else i[1].MEDIA_FINAL	 
			#alguns valores de media_final não são confiaveis na tabela .33
			nota = 0 if nota > 100 else nota 
			notas.append(nota) 

	if len(notas) != 0: 
		notas_np = np.array(notas) 
		media_np = np.mean(notas_np) 
		desvio_np = np.std(notas_np) 
		media = 0.0 if np.isnan(media_np) else media_np 
		desvio = 0.0 if np.isnan(desvio_np) else desvio_np 
		disciplina[index] = [media,desvio]	
	else:
		disciplina[index] = [0.0,0.0]  


def analises_gerais(df,lista_disciplinas):
	qtd_geral= df.groupby(["COD_ATIV_CURRIC","SITUACAO"]).size().reset_index(name="qtd" ) 
	qtd_ultimo_geral = \
	df.groupby(["COD_ATIV_CURRIC","SITUACAO","ANO"]).size().reset_index(name="qtd")  
	matr_por_semestre = \
	df.groupby(["COD_ATIV_CURRIC","ANO"]).size().reset_index(name="matr") 
	""" dataframe com a quantidade de matriculas por periodo e ano, por exemplo
	disciplina ci055 2010/1 teve x matriculas""" 
	"""Dataframes relacionado a notas.O campo qtd é inutil, o groupby pede se
	que se use um apply sobre o groupby, pois se não o grouby é tratado como
	objeto e não como um dataframe	""" 
	nota_geral_df = df.groupby(["COD_ATIV_CURRIC","MEDIA_FINAL", "SITUACAO",
			]).size().reset_index(name = "qtd" )  
	nota_semestral_df = df.groupby(["COD_ATIV_CURRIC","ANO", "MEDIA_FINAL", "SITUACAO",
			]).size().reset_index(name = "qtd" )  
	for disciplina in lista_disciplinas.keys():
		disciplina_dict = {} #facilitar os calculos 

		qtd  = qtd_geral.loc[qtd_geral.COD_ATIV_CURRIC == disciplina] 

		disciplina_semestral = qtd_ultimo_geral.loc[qtd_ultimo_geral.COD_ATIV_CURRIC == \
				disciplina] 

		ano = datetime.now().year - 1

		qtd_ultimo = disciplina_semestral.loc[disciplina_semestral.ANO == ano] 


		#quantidade de alunos
		qtd_matriculas = lista_disciplinas[disciplina]["qtd_alunos"]  


		#qtd é um dataframe que contem a ocorrencia de cada situacao
		qtd  = qtd_geral.loc[qtd_geral.COD_ATIV_CURRIC == disciplina] 

		#faz analises relacionada ao conhecimento
		conhecimento(qtd,disciplina_dict) 

		# faz analises relacionada ao trancamento
		trancamento(qtd,disciplina_dict,qtd_matriculas) 

		# faz analises relacionada a reprovacoes
		reprovacao(qtd,disciplina_dict,qtd_matriculas,"taxa_reprovacao_absoluta","taxa_reprovacao_frequencia") 
		qtd_matr_ultimo = matr_por_semestre.loc[(matr_por_semestre.COD_ATIV_CURRIC \
			== disciplina) & matr_por_semestre.ANO == ano]

		if qtd_matr_ultimo.empty: #caso a disciplina nao foi ofertada no ultimo ano
			disciplina_dict["taxa_reprovacao_ultimo_absoluta"] = -1  
			disciplina_dict["taxa_reprovacao_ultimo_frequencia"] = -1  
		else:
			reprovacao(qtd_ultimo,disciplina_dict,qtd_matriculas,"taxa_reprovacao_ultimo_absoluta",
					"taxa_reprovacao_ultimo_frequencia") 

		#faz as analises relacionada a nota
		nota_df = nota_geral_df.loc[nota_geral_df.COD_ATIV_CURRIC == disciplina] 
		nota_por_semestre_df = nota_semestral_df.loc[nota_semestral_df.COD_ATIV_CURRIC == disciplina] 
		nota_ultimo = nota_por_semestre_df.loc[nota_por_semestre_df.ANO ==
				ano] 

		nota(nota_df,disciplina_dict,"nota") 
		if nota_ultimo.empty:
			disciplina_dict["nota_ultimo_ano"] = -1 
		nota(nota_ultimo,disciplina_dict,"nota_ultimo_ano") 


		lista_disciplinas[disciplina].update(disciplina_dict)
#	*cursada ate a aprovacao
def analises_semestrais(df,lista_disciplinas):
	# [ ] -> nota media de aprovaçao 
	geral_df = \
	df.groupby(["COD_ATIV_CURRIC","ANO","PERIODO"]).size().reset_index(name
			= "matr" ) 
	df_semestral = df.groupby(["COD_ATIV_CURRIC", "ANO", "PERIODO" ,
	   "SITUACAO"]).size().reset_index(name = "qtds" ) 
	disciplinas = {} 
	for i in df_semestral.iterrows(): # percorre o dataframe
		disciplina = i[1].COD_ATIV_CURRIC #nome da disciplina
		if not(disciplina in disciplinas):
			disciplinas[disciplina] = {} 

		# para chave do dicionario ser do formato ano/periodo
		ano = str(int(i[1].ANO)) 
		periodo = str(i[1].PERIODO)   
		periodo_curso = ano+"/"+periodo # chave do dicionario

		situacao = i[1].SITUACAO 
		#verifica se a chave ano/periodo exitste no dicionario
		if not(periodo_curso in disciplinas[disciplina] ): 
			disciplinas[disciplina][periodo_curso]	= [0,0] #qtd aprovado,total
				
		# se a situacao for igual a aprovado entao qtd de aprovados em
		# ano/periodo +1
		if situacao in sit.SITUATION_PASS:
			disciplinas[disciplina][periodo_curso][0] += 1 # qtd de aprovados
		
		#quantidade total de matriculas no periodo ano/periodo
		disciplinas[disciplina][periodo_curso][1] += 1

	for disciplina in disciplinas.keys(): 
		for ano_periodo in disciplinas[disciplina].keys():	
			qtd_total = disciplinas[disciplina][ano_periodo][1]
			qtd_aprovados = disciplinas[disciplina][ano_periodo][0]
			#calcula a taxa de aprovacao por semestre, qtd_aprov/qtd_total 
			if qtd_total != 0:
				disciplinas[disciplina][ano_periodo][0] = qtd_aprovados / qtd_total
			else:
				disciplinas[disciplina][ano_periodo][0] = 0.0
				
		aprovacao_semestral = disciplinas[disciplina]	
		lista_disciplinas[disciplina]["aprovacao_semestral"] = aprovacao_semestral
def transforma_json(lista_disciplinas):
	for disciplina in lista_disciplinas.keys():
		disciplina_dict =lista_disciplinas[disciplina] 
		with open('cache/'+disciplina+'.json','w') as f:
			f.write(json.dumps(lista_disciplinas[disciplina],indent=4))
def listagem_disciplina(df,lista_disciplinas):
	listagem = {} 
	compara_aprov = {} 
	compara_nota = {} 
	cache = {} 
	disciplinas = {} 
	# nota media de todas as disciplinas
	trancamento = []
	reprovacao = []
	conhecimento = []
	nota= [] # lista que contem todas as notas medias de todas as disciplinas
	nota_desvio = [] # lista que contem todos os desvio padrao de todas as disciplinas 
	grafico(df,lista_disciplinas) 

	for disciplina in lista_disciplinas.keys(): 
		disciplina_dict = lista_disciplinas[disciplina] 
		cache[disciplina] = {
			"name": disciplina_dict["disciplina_nome"],
			"nota": disciplina_dict["nota"],
			"taxa_reprovacao_absoluta": disciplina_dict["taxa_reprovacao_absoluta"],
			"taxa_reprovacao_frequencia": disciplina_dict["taxa_reprovacao_frequencia"],
			"taxa_trancamento": disciplina_dict["taxa_trancamento"]
		}
		compara_disciplina = [] 
		compara_nota[disciplina]= lista_disciplinas[disciplina]["compara_nota"]  
		#calcula aprovacao semestral
		for ano in disciplina_dict["aprovacao_semestral"].keys():  
			aprov_por_ano = [ano,disciplina_dict["aprovacao_semestral"][ano][0]] 
			compara_disciplina.append(aprov_por_ano) 

		compara_aprov[disciplina] = compara_disciplina 
		disciplinas[disciplina] = disciplina_dict["disciplina_nome"]  

		# pega todas as taxas adiciona em uma lista, que depois será tranformada
		# em numpy array para poder uutilizar os metodos np.mean e np.std
		conhecimento.append(disciplina_dict["taxa_conhecimento"])
		trancamento.append(disciplina_dict["taxa_trancamento" ])
		reprovacao.append(disciplina_dict["taxa_reprovacao_absoluta" ])
		nota.append(disciplina_dict["nota"][0])  

	#nota
	nota_np = np.array(nota) 
	nota_media= np.mean(nota_np) 
	nota_desvio= np.std(nota_np) 
	#trancamento
	trancamento_np = np.array(trancamento) 
	trancamento_media = np.mean(trancamento_np) 
	trancamento_desvio = np.std(trancamento_np) 
	#conhecimento
	conhecimento_np = np.array(trancamento) 
	conhecimento_media = np.mean(trancamento_np) 
	conhecimento_desvio = np.std(trancamento_np) 
	#reprovacao
	reprovacao_np = np.array(trancamento) 
	reprovacao_media = np.mean(trancamento_np) 
	reprovacao_desvio = np.std(trancamento_np) 

	#verificar se o resultado final não é nan

	listagem = { "cache" : cache,
			"compara_aprov":  compara_aprov,
			"compara_nota": compara_nota, 
			"disciplinas": disciplinas,
			"taxa_conhecimento":[float(conhecimento_media),float(conhecimento_desvio)] ,
			"taxa_trancamento":[float(trancamento_media),float(trancamento_desvio)] ,
			"taxa_reprovacao":[float(reprovacao_media),float(reprovacao_desvio)] ,
			"nota": [float(nota_media),float(nota_desvio)] 
			} 
	return listagem

