# -*- coding: utf-8 -*-
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
#    df_quantidade = df.groupby(['COD_ATIV_CURRIC', 'SITUACAO']
#                             ).size().reset_index(name='Quantidades')
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
#    '''imprime todo o dataframe, por default o pandas so imprime as
#    10 linhas inicias a 10 finais, com essa funcao o pandas imprime
#    as linhas '''
#    with pd.option_context('display.max_rows', None, 'display.max_columns', 27):
#        print(d)
#
## calcula as taxas
#def func(x, matr):
#    ''' esta funcao recebe como parametro uma linha do dataframe e a
#quantidade de matriculas '''
#    c = matr[x['COD_ATIV_CURRIC']].values[0]
#    return (x['Quantidade'] / c)
#
## quantidade de matriculas
#def counts_matr(df):
#    return df.groupby(['COD_ATIV_CURRIC']).size()
#
## taxas e quantidades semetrais
#def analysis(df):
#    qnt_matr = counts_matr(df)  # quantidade de matriculas disciplina
#    ''' conta quantas vezes os valores de 'SITUACAO' se repete para
#    cada disciplina'''
#    disciplinas = df.groupby(['COD_ATIV_CURRIC', 'SITUACAO']
#                             ).size().reset_index(name='Quantidade')
#    ''' adiciona mais uma coluna ao df disciplina com as taxas de cada valor
#     de 'SITUACAO' '''
#    disciplina = disciplinas.groupby(['COD_ATIV_CURRIC', 'SITUACAO', 'Quantidade']).apply(
#        lambda x: func(x, qnt_matr)).reset_index(name='Taxas gerais')
#    disciplina = disciplina.drop('level_3',1) # retira coluna duplicada do index
#    # codigo que transforma o dataframe em um dicionario
#    dict_disciplina = {}
#    for dis in qnt_matr.keys():
#         # separa o dataframe em disciplina
#        disc = disciplina.loc[disciplina['COD_ATIV_CURRIC']==dis]
#        disc = disc.drop('COD_ATIV_CURRIC',1) # elimina a coluna codigo
#        # seta a coluna SITUACAO como index
#        disc = disc.set_index('SITUACAO').to_dict()
#        # para caso uma discipl. nao tenha um campo, coloca o campo com valor 0
#        for i in Situation.SITUATIONS:
#            if not(i[0] in disc['Quantidade'].keys()):
#                disc['Quantidade'][i[0]] = 0
#                disc['Taxas gerais'][i[0]] = 0
#        dict_disciplina[dis] = disc
#    return dict_disciplina
#
## quantidade de vezes cursadas ate obter a aprovacao
#def qnt_aprov(df):
#    qnt = df.groupby(['MATR_ALUNO', 'COD_ATIV_CURRIC']
#                     ).size().reset_index(name='qnt_aprov')
#    return qnt
## transforma o dataframe geral em json, # TODO: fazer o mesmo com o semestral
#def df_to_json(disciplina,qnt_matr):
#        # cria o json
#        with open(dis+'.json','w') as f:
#            json.dump(disc,f,indent=4)
#
#def matr_semestre(df):
#    return df.groupby(['COD_ATIV_CURRIC', 'PERIODO', 'ANO']).size()
#
#
#def func_semestre(x, matr):
#    # print (matr)
#    ano = int(x['ANO'])
#    # print(ano)
#    periodo = x['PERIODO'].values[0]
#    disciplina = x['COD_ATIV_CURRIC'].values[0]
#    c = matr[disciplina,periodo,ano]
#    return (x['counts_semestre'] / c)
#
#
#def analysis_semestre(df):
#    qnt_matr_semestre = matr_semestre(df)
#    discipline_semestre = df.groupby(['COD_ATIV_CURRIC', 'PERIODO', 'ANO', 'SITUACAO'])
#    discipline_semestre = discipline_semestre.size()
#
#    discipline_semestre = discipline_semestre.reset_index(name='counts_semestre')
#
#    discipline_semestre = discipline_semestre.groupby(['COD_ATIV_CURRIC', 'PERIODO', 'ANO', 'SITUACAO'])
#
#    discipline_semestre = discipline_semestre.apply(lambda x: func_semestre(x, qnt_matr_semestre))
#
#    discipline_semestre = discipline_semestre.reset_index(name='taxas_semetrais')
#    for dis in qnt_matr_semestre.keys():
#        dis = ['CI055']
#        disc = discipline_semestre.loc[discipline_semestre['COD_ATIV_CURRIC']==dis[0]].drop('COD_ATIV_CURRIC',1) # elimina a coluna codigo
#        disc = disc.drop('level_4',1)
#        print(dis[0])
#        print(disc.set_index('ANO'))
#        # seta a coluna SITUACAO como index
#        disc = disc.set_index('ANO').to_dict('index')
#        # with open(dis+'.json','w') as f:
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
    disciplinas = df.groupby(['COD_ATIV_CURRIC']).size()  
    for disciplina in disciplinas.index:
        disciplina_dict = {} 
        disciplina_df = df.loc[df.COD_ATIV_CURRIC == disciplina] 
        disciplina_dict['qtd_alunos'] = disciplinas[disciplina]   
        disciplina_dict['disciplina_codigo'] = disciplina 
        disciplina_dict['disciplina_nome'] = \
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
            sit.SIT_CONHECIMENTO_APROVADO].set_index('COD_ATIV_CURRIC' ) 
    disciplina_dict['qtd_conhecimento'] = total_conheci 

    if (total_conheci !=0) and (not conheci_aprov.empty):
        disciplina_dict['taxa_conhecimento'] = conheci_aprov.qtd.values[0] / total_conheci 
    else:
        disciplina_dict['taxa_conhecimento'] = 0.0

def trancamento(qtd,disciplina_dict,qtd_matr):
    trancamento_df = qtd.loc[(qtd.SITUACAO == sit.SIT_TRANCAMENTO_ADMINISTRATIVO) | 
                        (qtd.SITUACAO == sit.SIT_TRANCAMENTO_TOTAL) | 
                        (qtd.SITUACAO == sit.SIT_CANCELADO)] 
    qtd_tranc = trancamento_df.qtd.sum() 
    if np.isnan(qtd_tranc):
        qtd_tranc = 0
    disciplina_dict['qtd_trancamento'] = qtd_tranc 
    disciplina_dict['taxa_trancamento'] = qtd_tranc / qtd_matr if qtd_matr else 0.0

 
def reprovacao(qtd,disciplina,qtd_matr,taxa_reprov_absoluta,taxa_reprov_freq): 
    '''existem as analises reprovacao absoluta, reprovacao por frequencia,  
    reprovacao absoluta, reprovacao por frequencia da ultima vez que a
    disciplina foi ofertada, a logica das analise sao a mesma so muda os valores
    do dataframe qtd e o nomes das chaves do dicionario,logo é possível reaproveitar
    o mesmo codigo para fazer analise geral e da ultima vez que foi ofertado.''' 
    sit_reprov = sit.SITUATION_FAIL + (sit.SIT_REPROVADO_SEM_NOTA,)
    reprov_df = qtd.loc[(qtd.SITUACAO == sit_reprov[0]) |
                        (qtd.SITUACAO == sit_reprov[1]) |
                        (qtd.SITUACAO == sit_reprov[2]) |
                        (qtd.SITUACAO == sit_reprov[3]) ]
    qtd_reprov_abso = reprov_df.qtd.sum() #quantidade de reprovacao absoluta
    qtd_reprov_freq = reprov_df.loc[reprov_df.SITUACAO == sit_reprov[1]] 
    if qtd_matr != 0:
        disciplina[taxa_reprov_absoluta] = 0.0 \
                if np.isnan(qtd_reprov_abso) else qtd_reprov_abso / qtd_matr
        disciplina[taxa_reprov_freq] = 0.0 \
                if qtd_reprov_freq.empty else qtd_reprov_freq.qtd.values[0] / qtd_matr
    else:
        disciplina[taxa_reprov_absoluta] = 0.0
        disciplina[taxa_reprov_freq] = 0.0 

def nota(notas,disciplina,index):
    notas_l = [] 
    for i in notas.iterrows():
        if i[1].SITUACAO in sit.SITUATION_AFFECT_IRA:
            if not(np.isnan(i[1].MEDIA_FINAL)):
                notas_l.append(i[1].MEDIA_FINAL) 
    notas_np = np.array(notas_l) 
    media = notas_np.mean() 
    desvio_padrao = notas_np.std() 
    disciplina[index] = [media,desvio_padrao]  



def analises_gerais(df,lista_disciplinas):
    ''' Os dataframes qtd_geral e qtd_ultimo_geral são dataframes que possuem
        as colunas em comun COD_ATIV_CURRIC e SITUACAO, o qtd_ultimo_geral
        possuem as colunas ano e periodo.Ambos os dataframes possui a coluna qtd
        que é a quantidade de vezes que cada situacao se repete por disciplina''' 
    qtd_geral= df.groupby(['COD_ATIV_CURRIC','SITUACAO']).size().reset_index(name='qtd' ) 
    qtd_ultimo_geral = \
    df.groupby(['COD_ATIV_CURRIC','SITUACAO','ANO','PERIODO']).size().reset_index(name='qtd')  
    matr_por_semestre = \
    df.groupby(['COD_ATIV_CURRIC','ANO','PERIODO']).size().reset_index(name='matr') 
    ''' dataframe com a quantidade de matriculas por periodo e ano, por exemplo
    disciplina ci055 2010/1 teve x matriculas''' 
    '''Dataframes relacionado a notas.O campo qtd é inutil, o groupby pede se
    que se use um apply sobre o groupby, pois se não o grouby é tratado como
    objeto e não como um dataframe  ''' 
    nota_geral_df = df.groupby(['COD_ATIV_CURRIC','MEDIA_FINAL', 'SITUACAO',
            ]).size().reset_index(name = 'qtd' )  
    nota_semestral_df = df.groupby(['COD_ATIV_CURRIC','ANO','PERIODO', 'MEDIA_FINAL', 'SITUACAO',
            ]).size().reset_index(name = 'qtd' )  
    for disciplina in lista_disciplinas.keys():
        disciplina_dict = {} #facilitar os calculos 

        qtd  = qtd_geral.loc[qtd_geral.COD_ATIV_CURRIC == disciplina] 

        disciplina_semestral = qtd_ultimo_geral.loc[qtd_ultimo_geral.COD_ATIV_CURRIC == \
                disciplina] 

        ano = np.amax(disciplina_semestral.ANO) 

        disciplina_ano = disciplina_semestral.loc[disciplina_semestral.ANO \
                == ano] 

        periodo = np.amax(disciplina_ano.PERIODO) 
        qtd_ultimo = disciplina_ano.loc[disciplina_ano.PERIODO == periodo] 

        #quantidade de alunos
        qtd_matriculas = lista_disciplinas[disciplina]['qtd_alunos']  

        qtd_matr_ultimo = \
        matr_por_semestre.loc[(matr_por_semestre.COD_ATIV_CURRIC == disciplina) &
                            (matr_por_semestre.ANO == ano) &
                            (matr_por_semestre.PERIODO == periodo)].matr.values[0] 

        #qtd é um dataframe que contem a ocorrencia de cada situacao
        qtd  = qtd_geral.loc[qtd_geral.COD_ATIV_CURRIC == disciplina] 

        #faz analises relacionada ao conhecimento
        conhecimento(qtd,disciplina_dict) 

        # faz analises relacionada ao trancamento
        trancamento(qtd,disciplina_dict,qtd_matriculas) 

        # faz analises relacionada a reprovacoes
        reprovacao(qtd,disciplina_dict,qtd_matriculas,'taxa_reprovacao_absoluta','taxa_reprovacao_frequencia') 
        reprovacao(qtd_ultimo,disciplina_dict,qtd_matriculas,'taxa_reprovacao_ultimo_absoluta',
                'taxa_reprovacao_ultimo_frequencia') 

        #faz as analises relacionada a nota
        nota_df = nota_geral_df.loc[nota_geral_df.COD_ATIV_CURRIC == disciplina] 
        nota_por_semestre_df = nota_semestral_df.loc[nota_semestral_df.COD_ATIV_CURRIC == disciplina] 
        nota_ultimo_df = nota_por_semestre_df.loc[nota_por_semestre_df.ANO ==
                ano] 
        periodo_nota = np.amax(nota_ultimo_df.PERIODO) 
        nota_ultimo = nota_ultimo_df.loc[nota_ultimo_df.PERIODO == periodo_nota] 

        nota(nota_df,disciplina_dict,'nota') 
        nota(nota_ultimo,disciplina_dict,'nota_ultimo_ano') 


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
def analises_semestrais(df,lista_disciplinas):
    geral_df = \
    df.groupby(['COD_ATIV_CURRIC','ANO','PERIODO']).size().reset_index(name
            = 'matr' ) 
    df_semestral = df.groupby(['COD_ATIV_CURRIC', 'ANO', 'PERIODO' ,
        'MEDIA_FINAL','SITUACAO']).size().reset_index(name = 'qtds' ) 
    disciplinas = {} 
    for count,i in enumerate(df_semestral.iterrows()): 
        disciplina = i[1].COD_ATIV_CURRIC
        if not(disciplina in disciplinas):
            disciplinas[disciplina] = {} 
        ano = str(int(i[1].ANO)) 
        periodo = str(i[1].PERIODO)   
        situacao = i[1].SITUACAO 
        media = i[1].MEDIA_FINAL 
        periodo_curso = ano+"/"+periodo 
        disciplinas[disciplina][periodo_curso]  = [0.0,0]  
        if situacao in sit.SITUATION_AFFECT_IRA:
            disciplinas[disciplina][periodo_curso][0] += media
            disciplinas[disciplina][periodo_curso][1] +=1
    for disciplina in disciplinas.keys(): 
        for ano_periodo in disciplinas[disciplina].keys():  
            qtd = disciplinas[disciplina][ano_periodo][1]
            disciplinas[disciplina][ano_periodo][0] = 0.0 if qtd == 0 else qtd

        aprovacao_semestral = disciplinas[disciplina] 
        lista_disciplinas[disciplina]['aprovacao_semestral'] = \
            aprovacao_semestral
#    -taxa aprovacao semestral
#    -quantidade de matricula por semestre
def analises_disciplinas(df):
    lista_disciplinas = {}
    informacoes_gerais(df,lista_disciplinas) 
    analises_gerais(df,lista_disciplinas) 
    analises_semestrais(df,lista_disciplinas) 
    for disciplina in lista_disciplinas.keys(): 
        pprint.pprint(lista_disciplinas[disciplina] ) 
        print("---------------------------------------" ) 
#    """tranformar para json """ 
