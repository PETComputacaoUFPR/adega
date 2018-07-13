from script.utils.utils import *
from script.utils.situations import *
from script.analysis.degree_analysis import *
from script.analysis.student_analysis import StudentAnalysis
from script.analysis.course_analysis import *
from script.analysis.admission_analysis import *

from collections import defaultdict

try:
    to_unicode = unicode
except NameError:
    to_unicode = str



student_analysis = None

def build_cache(dataframe,path):
#   os.chdir("../src")
    ensure_path_exists(path)

    student_analysis = StudentAnalysis(dataframe)

    for cod, df in dataframe.groupby('COD_CURSO'):
        path = path + '/'
        generate_degree_data(path, df)
        generate_student_data(path+'students/', dataframe, student_analysis)
        generate_admission_data(path+'/admission/',df)
        generate_course_data(path+'disciplina/' ,dataframe)

def generate_degree_data(path, dataframe):
    ensure_path_exists(path)
    ensure_path_exists(path+'students')

    students = dataframe[['MATR_ALUNO', 'FORMA_EVASAO']].drop_duplicates()
    build_degree_json(path,dataframe)

def historico(dataframe):
    res = []

    for _, row in dataframe.iterrows():
        res.append(dict(row[['ANO', 'MEDIA_FINAL', 'PERIODO', 'SITUACAO', 'COD_ATIV_CURRIC', 'NOME_ATIV_CURRIC',
                             'CREDITOS', 'CH_TOTAL', 'DESCR_ESTRUTURA', 'FREQUENCIA']]))

    return res


def process_semestre(per, df):
    ira = df[df.SITUACAO.isin(Situation.SITUATION_AFFECT_IRA)].MEDIA_FINAL.mean()
    completas = df[df.SITUACAO.isin(Situation.SITUATION_PASS)].shape[0]
    tentativas = df[df.SITUACAO.isin(Situation.SITUATION_COURSED)].shape[0]

    return {
        'semestre': per,
        'ira': ira,
        'completas': completas,
        'tentativas': tentativas,
        'aprovacao': completas/tentativas if tentativas else 0,
        'ira_por_quantidade_disciplinas': ira/tentativas if tentativas else 0
    }



def generate_student_data(path, dataframe, student_analysis):
    student_data = defaultdict(dict)
    all_grrs = list(dataframe["MATR_ALUNO"].drop_duplicates())
    for x in all_grrs:
        student_data[x] = dict()
    
    analysis = [
        # tuple that contains in the first element the function that returns a dictionary with {"GRR": value}
        # and in the second position the name that this analysis will have in json

        # (student_analysis.posicao_turmaIngresso_semestral(),
        # "posicao_turmaIngresso_semestral"),

        (student_analysis.periodo_real(),
        "periodo_real"),

        (student_analysis.periodo_pretendido(),
        "periodo_pretendido"),

        (student_analysis.ira_semestral(),
        "ira_semestral"),

        (student_analysis.ira_por_quantidade_disciplinas(),
        "ira_por_quantidade_disciplinas"),

        (student_analysis.indice_aprovacao_semestral(),
        "indice_aprovacao_semestral"),

        (student_analysis.aluno_turmas(),
        "aluno_turmas"),

        (student_analysis.taxa_aprovacao(),
        "taxa_aprovacao"),

        (student_analysis.student_info(),
        "student"),
    ]
    
    for x in student_data:
        for a in analysis:                      # Use this to verify
            student_data[x][a[1]] = a[0][x]     # null fields in analysis
        save_json(path+x+".json", student_data[x])

    files_list = [
        EvasionForm.EF_ABANDONO,
        EvasionForm.EF_DESISTENCIA,
        EvasionForm.EF_FORMATURA,
        EvasionForm.EF_ATIVO,
        EvasionForm.EF_OUTROS
    ]

    list_situations = student_analysis.list_students()
    for fl in files_list:
        list_name = EvasionForm.code_to_str(int(fl))
        list_content = []
        if(fl in list_situations):
            list_content = list_situations[fl]

        save_json(path+"list/"+list_name+".json", list_content)




    #Falta verificar se alguem nao recebeu algumas analises

def generate_student_list(path):
    pass

def generate_admission_data(path,df):

    listagem = []

    analises = [
        ("ira", media_ira_turma_ingresso(df)),
        ("desvio_padrao", desvio_padrao_turma_ingresso(df)),
    ]

    # cria um dicionario com as analises para cada turma
    turmas = defaultdict(dict)
    for a in analises:
        for x in a[1]:
            turmas[x][ a[0] ] = a[1][x]

    listagem = []

    for t in turmas:
        resumo_turma = {
            "ano": x[0],
            "semestre": x[1]
        }

        for analise in turmas[t]:
            resumo_turma[analise] = turmas[t][analise]

        listagem.append(resumo_turma)

    save_json(path+"lista_turma_ingresso.json", listagem)


def generate_admission_list(path,df):
    pass

def generate_course_data(path,df):
    lista_disciplinas = {}
    informacoes_gerais(df,lista_disciplinas)
    analises_gerais(df,lista_disciplinas)
    analises_semestrais(df,lista_disciplinas)

    for disciplina in lista_disciplinas.keys():
        save_json(path+disciplina+'.json',lista_disciplinas[disciplina])

    disciplinas = listagem_disciplina(df,lista_disciplinas)
    save_json(path+'disciplinas.json',disciplinas)
