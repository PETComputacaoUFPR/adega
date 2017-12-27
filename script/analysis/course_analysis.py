# -*- coding: utf-8 -*-
from datetime import datetime
import pprint
import pandas as pd
import json
import numpy as np
from utils.situations import Situation as sit
#funcoes
#
#    make_taxas -- parametros df e ultima turma ingresso
#    *qtd_alunos 
#    *qtd_trancamento 
#    *taxa_reprovacao_absoluta 
#    *taxa_reprovacao_frequencia 
#    *taxa_reprovacao_ultimo_absoluto 
#    *taxa_reprovacao_ultimo_frequencia 
#    *taxa_trancamento 
##listas_disciplinas é dicionario com todas as disciplinas
#def taxas_gerais(df,ultima_turma_ingresso,lista_disciplina):
#    df_quantidade = df.groupby(["COD_ATIV_CURRIC", "SITUACAO"]
#                             ).size().reset_index(name="Quantidades")
#    for disciplina in lista_disciplina.keys:
#        quantidades = df_quantidade.loc[df_quantidade.COD_ATIV_CURRIC == disciplina] 
#        
#        qtd_trancamento_df =quantidades.loc[quantidades.SITUACAO ==
#                (sit.SIT_CANCELADO || sit.SIT_TRANCAMENTO_ADMINISTRATIVO ||
#                    sit.SIT_TRANCAMENTO_TOTAL) ] 
#        qtd_trancamento = qtd_trancamento_df.sum
#
#        qtd_conhecimento_aprov = quantidades.loc[quantidades.SITUACAO ==
#                sit.SIT_CONHECIMENTO_APROVADO].Quantidade
#        qtd_conhecimento_reprov = quantidades.loc[quantidades.SITUACAO ==
#                sit.SIT_CONHECIMENTO_REPROVADO].Quantidade 
#        lista_disciplina[disciplina][qtd_conhecimento] = qtd_conhecimento_aprov
#        + qtd_conhecimento_reprov
#        if qtd_conhecimento:
#            taxa_conhecimento = qtd_conhecimento_aprov / listas_disciplinas[disciplina][qtd_conhecimento] 
#        else:
#            taxa_conhecimento = -1
#
#def print_analise(d):
#    """imprime todo o dataframe, por default o pandas so imprime as
#    10 linhas inicias a 10 finais, com essa funcao o pandas imprime
#    as linhas """
#    with pd.option_context("display.max_rows", None, "display.max_columns", 27):
#        print(d)
#
## calcula as taxas
#def func(x, matr):
#    """ esta funcao recebe como parametro uma linha do dataframe e a
#quantidade de matriculas """
#    c = matr[x["COD_ATIV_CURRIC"]].values[0]
#    return (x["Quantidade"] / c)
#
## quantidade de matriculas
#def counts_matr(df):
#    return df.groupby(["COD_ATIV_CURRIC"]).size()
#
## taxas e quantidades semetrais
#def analysis(df):
#    qnt_matr = counts_matr(df)  # quantidade de matriculas disciplina
#    """ conta quantas vezes os valores de "SITUACAO" se repete para
#    cada disciplina"""
#    disciplinas = df.groupby(["COD_ATIV_CURRIC", "SITUACAO"]
#                             ).size().reset_index(name="Quantidade")
#    """ adiciona mais uma coluna ao df disciplina com as taxas de cada valor
#     de "SITUACAO" """
#    disciplina = disciplinas.groupby(["COD_ATIV_CURRIC", "SITUACAO", "Quantidade"]).apply(
#        lambda x: func(x, qnt_matr)).reset_index(name="Taxas gerais")
#    disciplina = disciplina.drop("level_3",1) # retira coluna duplicada do index
#    # codigo que transforma o dataframe em um dicionario
#    dict_disciplina = {}
#    for dis in qnt_matr.keys():
#         # separa o dataframe em disciplina
#        disc = disciplina.loc[disciplina["COD_ATIV_CURRIC"]==dis]
#        disc = disc.drop("COD_ATIV_CURRIC",1) # elimina a coluna codigo
#        # seta a coluna SITUACAO como index
#        disc = disc.set_index("SITUACAO").to_dict()
#        # para caso uma discipl. nao tenha um campo, coloca o campo com valor 0
#        for i in Situation.SITUATIONS:
#            if not(i[0] in disc["Quantidade"].keys()):
#                disc["Quantidade"][i[0]] = 0
#                disc["Taxas gerais"][i[0]] = 0
#        dict_disciplina[dis] = disc
#    return dict_disciplina
#
## quantidade de vezes cursadas ate obter a aprovacao
#def qnt_aprov(df):
#    qnt = df.groupby(["MATR_ALUNO", "COD_ATIV_CURRIC"]
#                     ).size().reset_index(name="qnt_aprov")
#    return qnt
## transforma o dataframe geral em json, # TODO: fazer o mesmo com o semestral
#def df_to_json(disciplina,qnt_matr):
#        # cria o json
#        with open(dis+".json","w") as f:
#            json.dump(disc,f,indent=4)
#
#def matr_semestre(df):
#    return df.groupby(["COD_ATIV_CURRIC", "PERIODO", "ANO"]).size()
#
#
#def func_semestre(x, matr):
#    # print (matr)
#    ano = int(x["ANO"])
#    # print(ano)
#    periodo = x["PERIODO"].values[0]
#    disciplina = x["COD_ATIV_CURRIC"].values[0]
#    c = matr[disciplina,periodo,ano]
#    return (x["counts_semestre"] / c)
#
#
#def analysis_semestre(df):
#    qnt_matr_semestre = matr_semestre(df)
#    discipline_semestre = df.groupby(["COD_ATIV_CURRIC", "PERIODO", "ANO", "SITUACAO"])
#    discipline_semestre = discipline_semestre.size()
#
#    discipline_semestre = discipline_semestre.reset_index(name="counts_semestre")
#
#    discipline_semestre = discipline_semestre.groupby(["COD_ATIV_CURRIC", "PERIODO", "ANO", "SITUACAO"])
#
#    discipline_semestre = discipline_semestre.apply(lambda x: func_semestre(x, qnt_matr_semestre))
#
#    discipline_semestre = discipline_semestre.reset_index(name="taxas_semetrais")
#    for dis in qnt_matr_semestre.keys():
#        dis = ["CI055"]
#        disc = discipline_semestre.loc[discipline_semestre["COD_ATIV_CURRIC"]==dis[0]].drop("COD_ATIV_CURRIC",1) # elimina a coluna codigo
#        disc = disc.drop("level_4",1)
#        print(dis[0])
#        print(disc.set_index("ANO"))
#        # seta a coluna SITUACAO como index
#        disc = disc.set_index("ANO").to_dict("index")
#        # with open(dis+".json","w") as f:
#            # json.dump(disc,f,indent=4)
#        print("--------------------------------------------------------------------------------")
#
#        break
#    return discipline_semestre
#
#
#
#def Main(df):
#
#    # Analysis = analysis(df)
#    Analysis_semestre = analysis_semestre(df)
#    # matr = counts_matr(df)
#    # df_to_json(Analysis,matr)
#    # matr_semes = matr_semestre(df)
#    # pprint_analise(matr_semes)
#
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
#    -nome da disciplina
#    -codigo da disciplina
#    -lista de disciplina
#    -quantidade de matriculas
#    -retorna um dicionario de disciplina, cada disciplina com quantidade de
#    matriculas
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

"analises que envolvem nota e disciplina, como nota media geral, nota media
ultima vez que foi ofertado, grafico de comparacao de intervalo/nota.
as diferença entre as analises nota media geral, desvio padrao geral para nota
media ultimo, desvio padrao ultimo é apenas a quandidade de linhas do nota_df e
o nome da chave no dicionario disciplina, logo eu passo o nome da chave como
parametro e mudo o notas_df, assim posso reutilizar o codigo.
O grafico compara_nota precisa de um notas_df geral, um laço que itera cada
lunha do dataframe e verifica em qual intervalo está a nota, logo se eu fizer um
if para verificar se o notas_df é geral ou ultimo, posso aproveitar fazer as
analises gerais e o grafico percorrendo uma unica vez o dataframe. A desvantagem
é de a função fugir de seu escopo." 
def nota(notas_df,disciplina,index,grafico,seme_geral):
    notas = [] 
    dic = {"00-4.9":0, "05-9.9":0, "10-14.9":0, "15-19.9":0, "20-24.9":0, "25-29.9":0, "30-34.9":0,
           "35-39.9":0, "40-44.9":0, "45-49.9":0, "50-54.9":0, "55-59.9":0, "60-64.9":0, "65-69.9":0,
           "70-74.9":0, "75-79.9":0, "80-84.9":0, "85-89.9":0, "90-94.9": 0,"95-100":0}
    for i in notas_df.iterrows():
        if i[1].SITUACAO in sit.SITUATION_AFFECT_IRA:
            if seme_geral: #True para quando nota_df é geral e False para quando é ultimo
                pass
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
    """ Os dataframes qtd_geral e qtd_ultimo_geral são dataframes que possuem
        as colunas em comun COD_ATIV_CURRIC e SITUACAO, o qtd_ultimo_geral
        possuem as colunas ano e periodo.Ambos os dataframes possui a coluna qtd
        que é a quantidade de vezes que cada situacao se repete por disciplina""" 
    qtd_geral= df.groupby(["COD_ATIV_CURRIC","SITUACAO"]).size().reset_index(name="qtd" ) 
    qtd_ultimo_geral = \
    df.groupby(["COD_ATIV_CURRIC","SITUACAO","ANO"]).size().reset_index(name="qtd")  
    matr_por_semestre = \
    df.groupby(["COD_ATIV_CURRIC","ANO"]).size().reset_index(name="matr") 
    """ dataframe com a quantidade de matriculas por periodo e ano, por exemplo
    disciplina ci055 2010/1 teve x matriculas""" 
    """Dataframes relacionado a notas.O campo qtd é inutil, o groupby pede se
    que se use um apply sobre o groupby, pois se não o grouby é tratado como
    objeto e não como um dataframe  """ 
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
#   -qtd_conhecimento
#   -qtd_trancamento
#   -taxa_conhecimento
#   -taxa_reprovacao_absoluta
#   -taxa_reprovacao_frequencia
#   -taxa_reprovacao_ultimo_absoluto
#   -taxa_reprovacao_ultimo_frequencia
#   -taxa_trancamento
#   -nota geral desvio padrao geral
#   -nota ultima vez ofertado e desvio padrao
#   *cursada ate a aprovacao
def analises_semestrais(df,lista_disciplinas):
    # [X] -> taxa de aprovacao semestral 
    # [ ] -> nota media de aprovaçao 
    geral_df = \
    df.groupby(["COD_ATIV_CURRIC","ANO","PERIODO"]).size().reset_index(name
            = "matr" ) 
    df_semestral = df.groupby(["COD_ATIV_CURRIC", "ANO", "PERIODO" ,
       "SITUACAO"]).size().reset_index(name = "qtds" ) 
    # df_semestral = df.groupby(["COD_ATIV_CURRIC", "ANO", "PERIODO" ,
    #     "MEDIA_FINAL","SITUACAO"]).size().reset_index(name = "qtds" ) 
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
            disciplinas[disciplina][periodo_curso]  = [0,0] #qtd aprovado,total
                
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
#    -taxa aprovacao semestral
#    -quantidade de matricula por semestre
def transforma_json(lista_disciplinas):
    for disciplina in lista_disciplinas.keys():
        disciplina_dict =lista_disciplinas[disciplina] 
        # for item in disciplina_dict.keys(): 
        #     print(item) 
        #     print(disciplina_dict[item])
        #     print(type(disciplina_dict[item])) 
        with open('cache/'+disciplina+'.json','w') as f:
            f.write(json.dumps(lista_disciplinas[disciplina],indent=4))
def listagem_disciplina(lista_disciplinas):
    listagem = {} 
    cache = {} 
    compara_aprov = {} 
    disciplinas = {} 
    # nota media de todas as disciplinas
    taxa_trancamento = 0.0
    taxa_reprovacao = 0.0
    taxa_conhecimento = 0.0
    nota_media = [] # lista que contem todas as notas medias de todas as disciplinas
    nota_desvio = [] # lista que contem todos os desvio padrao de todas as disciplinas 

    for disciplina in lista_disciplinas.keys(): 
        disciplina_dict = lista_disciplinas[disciplina] 

        cache[disciplina] = {"nota":disciplina_dict["nota"],
                "taxa_reprovacao_absoluta":disciplina_dict["taxa_reprovacao_absoluta"],
                "taxa_reprovacao_frequencia": disciplina_dict["taxa_reprovacao_frequencia" ],
                "taxa_trancamento":disciplina_dict["taxa_trancamento"]}  
        compara_disciplina = [] 
        
        #calcula aprovacao semestral
        for ano in disciplina_dict["aprovacao_semestral"].keys():  
            aprov_por_ano = [ano,disciplina_dict["aprovacao_semestral"][ano][0]] 
            compara_disciplina.append(aprov_por_ano) 

        compara_aprov[disciplina] = compara_disciplina 
        disciplinas[disciplina] = disciplina_dict["disciplina_nome"]  

        taxa_conhecimento += disciplina_dict["taxa_conhecimento"] 
        taxa_trancamento += disciplina_dict["taxa_trancamento" ] 
        taxa_reprovacao += disciplina_dict["taxa_reprovacao_absoluta" ] 
        nota_media.append(disciplina_dict["nota"][0])  
        nota_desvio.append(disciplina_dict["nota"][1])  
        #print(disciplina_dict["nota"][0])  
        #print(disciplina_dict["nota"][1])  

    #transformando as listas nota_media e nota_desvio para numpy array, para
    #poder utilizar os metodos np.mean()  e np.std() por questão de desepenho. 
    nota_media_np = np.array(nota_media) 
    nota_desvio_np = np.array(nota_desvio) 
    media= np.mean(nota_media_np) 
    desvio= np.std(nota_desvio_np) 
    #verifica se o resultado final não é nan
    if np.isnan(media):
        media = 0.0
    if np.isnan(desvio):
        desvio = 0.0

    #calcula os valores medios das taxas de todas as disciplinas
    qtd_disciplina = len(lista_disciplinas.keys()) 
    if qtd_disciplina != 0:
        taxa_conhecimento /= qtd_disciplina 
        taxa_trancamento /= qtd_disciplina
        taxa_reprovacao /= qtd_disciplina

    listagem = { "cache" : cache,
            "compara_aprov":  compara_aprov,
            "disciplinas": disciplinas,
            "taxa_conhecimento":taxa_conhecimento,
            "taxa_trancamento":taxa_trancamento,
            "taxa_reprovacao": taxa_reprovacao, 
            "nota": [float(media),float(desvio) ] 
            } 
    with open("cache/disciplinas.json",'w') as f:
        f.write(json.dumps(listagem,indent=4)) 
 # [ ] ->media_disc
 # [ ] compara_aprov 

def analises_disciplinas(df):
    lista_disciplinas = {}
    informacoes_gerais(df,lista_disciplinas) 
    analises_gerais(df,lista_disciplinas) 
    analises_semestrais(df,lista_disciplinas) 
    transforma_json(lista_disciplinas) 
    listagem_disciplina(lista_disciplinas) 

#    for disciplina in lista_disciplinas.keys(): 
#        pprint.pprint(lista_disciplinas[disciplina] ) 
#        print("---------------------------------------" ) 
#    """tranformar para json """ 
