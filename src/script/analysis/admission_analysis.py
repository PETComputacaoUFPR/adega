import numpy as np

from script.utils.situations import *
from script.analysis.student_analysis import StudentAnalysis
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
    student_analysis = StudentAnalysis(df)
    iras = student_analysis.ira_alunos()

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

def evasion_per_semester(df):
    # filtra a planilha, deixando apenas 1 linha por estudante por periodo que ele passou desde que entrou no curso
    turmas_ingresso = df.drop_duplicates(['ANO_INGRESSO_y','SEMESTRE_INGRESSO', 'ANO','PERIODO', 'MATR_ALUNO'], keep='last')
    # agrupa as linhas do dataframe resultante da filtragem pela tupla (ano de entrada, periodo de entrada, ano, periodo)
    t_i_semestral_size = turmas_ingresso.groupby(['ANO_INGRESSO_y','SEMESTRE_INGRESSO', 'ANO','PERIODO'])['MATR_ALUNO']
    # filtra o dataframe, deixando apenas 1 linha por estudante que evadiu
    t_i_evasions = turmas_ingresso.loc[(turmas_ingresso.FORMA_EVASAO != EvasionForm.EF_ATIVO) & (turmas_ingresso.FORMA_EVASAO != EvasionForm.EF_FORMATURA) & (turmas_ingresso.FORMA_EVASAO != EvasionForm.EF_REINTEGRACAO)]
    # agrupa as linhas do dataframe de evadidos indexados pela tupla (ano de entrada, periodo de entrada, ano, periodo), conta o numero de linhas e transforma isso em um dicionario
    t_i_evasions_semestral_size = t_i_evasions.groupby(['ANO_INGRESSO_y','SEMESTRE_INGRESSO', 'ANO_EVASAO','SEMESTRE_EVASAO'])['MATR_ALUNO'].nunique().to_dict()
    dict_evasion = {}
    aux = {}
    # transforma o groupby em um dicionario que contem a evasao dividida pelo numero de linhas de cada grupo do agrupamento, indexado pela tupla de tuplas ((ano de entrada, periodo de entrada), (ano, periodo))
    for t_i_s in t_i_semestral_size:
        # trata os campos 2 e 3 da tupla (ano de entrada, periodo de entrada, ano, periodo) para que fique no mesmo formato que as chaves do dicionario t_i_evasions_semestral_size
        t_i_s_aux = (t_i_s[0][0], t_i_s[0][1], str(t_i_s[0][2]), t_i_s[0][3].split("o")[0])
        # pega o numero de evasoes de acordo com a tupla (ano de entrada, periodo de entrada, ano, periodo)
        if t_i_s_aux in t_i_evasions_semestral_size:
            evasions = t_i_evasions_semestral_size[t_i_s_aux]
        else:
            evasions = 0
        aux.update({((t_i_s[0][0], t_i_s[0][1]), (t_i_s[0][2], t_i_s[0][3])):(evasions/t_i_s[1].size)})
    # transforma o dicionario anterior em um outro dicionario, indexado pela tupla (ano de entrada, periodo de entrada), tendo como elementos outros dicionarios.
    # cada dicionario contido no dicionario e indexado pela tupla (ano, periodo) e contem a evasao dividida pelo numero de linhas de cada grupo do agrupamento
    for t_i_s, value in aux.items():
        dict_evasion.setdefault(t_i_s[0], {})[t_i_s[1]] = value
    return dict_evasion
