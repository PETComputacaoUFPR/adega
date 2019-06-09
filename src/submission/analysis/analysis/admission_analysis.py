from submission.analysis.utils.situations import Situation as sit
from submission.analysis.utils.situations import EvasionForm as ef
from submission.analysis.utils.situations import *
from submission.analysis.utils.situations import Situation as sit
from submission.analysis.utils.situations import EvasionForm as ef
from submission.analysis.analysis.student_analysis import StudentAnalysis
from collections import defaultdict

import numpy as np



class Admission(object):
    __dataframes = {}
    __groupbys = {}
    analysis = {}
    __counts = False # se as quantidades já foram calculadas
    def __init__(self, df):
        self.__dataframes["df_original"] = df
        self.__dataframes["df_filted"] = df.drop_duplicates(["MATR_ALUNO"])
        self.__groupbys["groupby_original"] = df.groupby(['ANO_INGRESSO_y', 'SEMESTRE_INGRESSO'])
        self.__groupbys["groupby_filted"] = self.__dataframes["df_filted"].groupby(['ANO_INGRESSO_y', 'SEMESTRE_INGRESSO'])
    def count_evasion_form(self, g, evasion_form):
        return g.apply(lambda x: x.loc[(x.FORMA_EVASAO == evasion_form)].shape[0])

    def counts(self):
        """
            Calcula as seguintes quantidades referente a turma ingresso:
                * Quantidade de alunos ativos
                * Quantidade de alunos de cada turma ingresso
                * Quantidade de alunos que abandonaram o curso
                * Quantidade de alunos que se formaram
                * Quantidade de alunos que evadiram
                * Quantidade de alunos que sairam do curso por outros motivos
                dos já citados
        """
        qtd_alunos_ingresso = self.__groupbys["groupby_filted"].apply(lambda x: x.shape[0])
        self.analysis["qtd_alunos_ingresso"] = qtd_alunos_ingresso
        evasions = [
            ("qtd_ativos", ef.EF_ATIVO),
            ("qtd_abandono", ef.EF_ABANDONO),
            ("qtd_formatura", ef.EF_FORMATURA),
            ("qtd_ativos", ef.EF_ATIVO)
            ]
        # calcula a quantidade de alunos qtd_ativos, qtd_abandono e qtd_formatura
        for i in evasions:
            self.analysis[i[0]] = self.count_evasion_form(self.__groupbys["groupby_filted"], i[1])

        # calcula a quantidade de alunos evadidos

        self.analysis["alunos_evadidos"] = qtd_alunos_ingresso - self.analysis["qtd_ativos"]
        self.analysis["outras_formas_evasao"] = self.analysis["alunos_evadidos"] - self.analysis["qtd_formatura"] - self.analysis["qtd_abandono"]
        self.__counts = True

    def taxa_evasao(self):
        """ Calcula a taxa de evasão de cada turma ingresso """
        # precisa das quantidades para calcular as taxas
        if not self.__counts:
            self.counts()
        # calcula a taxa de evasão da turma ingresso
        qtd_alunos = self.analysis["qtd_alunos_ingresso"]
        qtd_evasao = self.analysis["alunos_evadidos"]
        taxa_evasao = qtd_evasao / qtd_alunos
        taxa_evasao[np.isnan(taxa_evasao)] = 0.0
        taxa_evasao[np.isinf(taxa_evasao)] = 0.0
        self.analysis["taxa_evasao"] = taxa_evasao

    def formatura_medio(self):
        """
            Calcula o tempo medio levado para cada turma ingresso se formar.
        """
        df = self.__dataframes["df_filted"]
        df = df.loc[df.FORMA_EVASAO == ef.EF_FORMATURA]

        # muda semestre 1 para 0.0 e semestre 2 para 0.5
        dict_convert = {"1":0.0, "2":0.5, "Anual":0.0}
        df["SEMESTRE_INGRESSO"] = df["SEMESTRE_INGRESSO"].map(dict_convert)
        df["SEMESTRE_EVASAO"] = df["SEMESTRE_EVASAO"].map(dict_convert)

        # agrupa dados por turma ingresso
        admission_g = df.groupby(["ANO_INGRESSO_y", "SEMESTRE_INGRESSO"])

        # faz a media do tempo gasto por cada aluno de cada turma ingresso na
        # graduação
        media_formatura = admission_g.apply(lambda x:\
                ((x.ANO_EVASAO.astype(float)+x.SEMESTRE_EVASAO.astype(float))-\
                (x.ANO_INGRESSO_y.astype(float)+x.SEMESTRE_INGRESSO.astype(float))).mean())
        self.analysis["media_formatura"] = media_formatura.rename({0.0: '1', 0.5:'2'})

    def taxa_reprovacao(self):
        if(not self.__counts):
            self.counts()

        # calcula a taxa de evasão da turma ingresso
        admission_g = self.__groupbys["groupby_original"]
        taxa_reprovacao = admission_g.apply(lambda x:\
                x[x.SITUACAO.isin(sit.SITUATION_FAIL)].shape[0] /\
                x[x.SITUACAO.isin(sit.SITUATION_COURSED)].shape[0])
        self.analysis["taxa_reprovacao"] = taxa_reprovacao

    def ira_medio(self):
        # filtra o dataframe pela situações que afetam o ira
        dataframe = self.__dataframes["df_original"][self.__dataframes["df_original"]['SITUACAO'].isin(sit.SITUATION_AFFECT_IRA)]
        submission_groupby = dataframe.groupby(["ANO_INGRESSO_y", "SEMESTRE_INGRESSO"])
        """ Para cada turma ingresso, faz o agrupamento por aluno e calcula o
        ira de cada aluno e depois é feito a media dos iras de todos os alunos
        da turma ingresso.
        Sao dois .apply, um dentro do outro, sendo que um intera sobre a turma
        ingresso e ai faz o agrupamento de alunos e o outro intera sobre os
        alunos da turma ingresso para calcular o ira. """
        
        ira_medio = submission_groupby.apply(lambda x:\
            x.groupby(["MATR_ALUNO"]).apply(lambda y:\
            (y.MEDIA_FINAL * y.TOTAL_CARGA_HORARIA).sum() /\
            (y.TOTAL_CARGA_HORARIA.sum()*100)).mean())

        self.analysis["ira_medio"] = ira_medio

    def admission_list(self):
        self.analysis["admission_list"] = list(self.__groupbys["groupby_filted"].groups.keys())


    def build_analysis(self):
        self.counts()
        self.admission_list()
        self.ira_medio()
        self.taxa_evasao()
        self.taxa_reprovacao()
        self.formatura_medio()

    def build_cache(self):
        admissions = []
        formatura_medio = self.analysis["media_formatura"]
        for i in self.analysis["admission_list"]:
            admission_dict = {}
            # This will create an directory when build_cache create the json
            # By instance: The files and directories admission/2010/1.json will
            # be created
            
            # The ira_medio can be undefined for some admissions
            # Then, we need to verify if it was computed 
            ira_medio = 0
            if i in self.analysis["ira_medio"].keys():
                ira_medio = self.analysis["ira_medio"][i]

            admission_dict["ano"] = i[0]
            admission_dict["semestre"] = i[1]
            admission_dict["abandono"] = int(self.analysis["qtd_abandono"][i])
            admission_dict["ativos"] = int(self.analysis["qtd_ativos"][i])
            admission_dict["formatura"] = int(self.analysis["qtd_formatura"][i])
            admission_dict["alunos_evadidos"] = int(self.analysis["alunos_evadidos"][i])
            admission_dict["outras_formas_evasao"] = int(self.analysis["outras_formas_evasao"][i])
            admission_dict["formatura_media"] = float(formatura_medio[i]) if i in formatura_medio.index else -1
            admission_dict["quantidade_alunos"] =  int(self.analysis["qtd_alunos_ingresso"][i])
            admission_dict["ira_medio"] = float(ira_medio)
            admission_dict["taxa_evasao"] = float(self.analysis["taxa_evasao"][i])
            admission_dict["taxa_reprovacao"] = float(self.analysis["taxa_reprovacao"][i])
            admissions.append(admission_dict)
        return admissions


    def build_cache_evasion_count(self):
        admission_dict = {}
        admission_dict["ano"] = {}
        admission_dict["semestre"] = {}
        admission_dict["quantidade_alunos"] = {}
        admission_dict["abandono"] = {}
        admission_dict["ativos"] = {}
        admission_dict["formatura"] = {}
        admission_dict["alunos_evadidos"] = {}
        admission_dict["outras_formas_evasao"] = {}
        for i in self.analysis["admission_list"]:
            admission_dict["ano"][i] = i[0]
            admission_dict["semestre"][i] = i[1]
            admission_dict["quantidade_alunos"][i] = int(self.analysis["qtd_alunos_ingresso"][i])
            admission_dict["abandono"][i] = int(self.analysis["qtd_abandono"][i])
            admission_dict["ativos"][i] = int(self.analysis["qtd_ativos"][i])
            admission_dict["formatura"][i] = int(self.analysis["qtd_formatura"][i])
            admission_dict["alunos_evadidos"][i] = int(self.analysis["alunos_evadidos"][i])
            admission_dict["outras_formas_evasao"][i] = int(self.analysis["outras_formas_evasao"][i])
        return admission_dict

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
            ira_class = []

            # Compute all individual IRA from an class
            for student in student_grouped:
                #TODO: Verify if this can be calculated without groupby
                ira_individual =(
                    (student[1].MEDIA_FINAL*student[1].TOTAL_CARGA_HORARIA).sum() )/(100*student[1].TOTAL_CARGA_HORARIA.sum()
                )
                ira_class.append(ira_individual)

            # Compute the mean and standard variation from an class
            # semester[0] represents a semester/year key
            dict_ira_semester.update({
                semester[0]: [
                    np.mean(ira_class),
                    np.std(ira_class)
                ]
            })

        dict_admission.update({admission[0]:dict_ira_semester})
    return dict_admission

def iras_alunos_turmas_ingressos(df, student_analysis):
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



def media_ira_turma_ingresso(df, student_analysis):
    iras_alunos_por_turma = iras_alunos_turmas_ingressos(df, student_analysis)
    # Calcula a média do ira para cada turma_ingresso
    resultados = {}
    for r in iras_alunos_por_turma:
        aux = np.array(iras_alunos_por_turma[r])
        resultados[r] = np.mean(aux)

    return resultados

def desvio_padrao_turma_ingresso(df, student_analysis):
    iras_alunos_por_turma = iras_alunos_turmas_ingressos(df, student_analysis)
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

def students_per_semester(df):
    # filtra a planilha, deixando apenas 1 linha por estudante por periodo que ele passou desde que entrou no curso
    turmas_ingresso = df.drop_duplicates(['ANO_INGRESSO_y', 'SEMESTRE_INGRESSO', 'ANO', 'PERIODO', 'MATR_ALUNO'], keep='last')
    # agrupa as linhas do dataframe resultante da filtragem pela tupla (ano de entrada, periodo de entrada, ano, periodo)
    t_i_semestral_size = turmas_ingresso.groupby(['ANO_INGRESSO_y', 'SEMESTRE_INGRESSO', 'ANO', 'PERIODO'])['MATR_ALUNO']
    dict_students = {}
    aux = {}
    # transforma o groupby em um dicionario que contem o numero de linhas de cada grupo do agrupamento, indexado pela tupla de tuplas ((ano de entrada, periodo de entrada), (ano, periodo))
    for t_i_s in t_i_semestral_size:
        aux.update({((t_i_s[0][0], t_i_s[0][1]), (t_i_s[0][2], t_i_s[0][3])):(t_i_s[1].size)})
    # transforma o dicionario anterior em um outro dicionario, indexado pela tupla (ano de entrada, periodo de entrada), tendo como elementos outros dicionarios.
    # cada dicionario contido no dicionario e indexado pela tupla (ano, periodo) e contem o numero de linhas de cada grupo do agrupamento
    for t_i_s, value in aux.items():
        dict_students.setdefault(t_i_s[0], {})[t_i_s[1]] = value
    return dict_students

def taxa_aprovacao(self, df=None):
    df = df if df is not None else self.data_frame

    aprovacoes_semestres = self.indice_aprovacao_semestral(df=df)

    for aluno in aprovacoes_semestres:
        total = sum([aprovacoes_semestres[aluno][s][1]
                        for s in aprovacoes_semestres[aluno]])
        aprovacoes = sum([aprovacoes_semestres[aluno][s][0]
                            for s in aprovacoes_semestres[aluno]])
        total = float(total)
        aprovacoes = float(aprovacoes)
        if(total != 0):
            aprovacoes_semestres[aluno] = aprovacoes/total
        else:
            aprovacoes_semestres[aluno] = None

    return aprovacoes_semestres
