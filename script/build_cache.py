

from utils.utils import *
from utils.situations import *
from analysis.degree_analysis import *
from analysis.student_analysis import *



try:
    to_unicode = unicode
except NameError:
    to_unicode = str


def build_cache(dataframe):
#    os.chdir("../src")
    path = 'cache/curso/'

    ensure_path_exists(path)

    for cod, df in dataframe.groupby('COD_CURSO'):
        generate_degree_data(path+'/'+cod+'/', df)

    #generate_degree_data(path, dataframe)
    #generate_student_data(path, dataframe)
    #generate_student_list(path)
    #generate_admission_data(path)
    #generate_admission_list(path)
    #generate_course_data(path)
    #generate_course_general_data(path)

def generate_degree_data(path, dataframe):
    ensure_path_exists(path)
    ensure_path_exists(path+'students')

    students = dataframe[['MATR_ALUNO', 'FORMA_EVASAO']].drop_duplicates()

    data = {
        'average_graduation': average_graduation(dataframe),
        'general_failure': general_failure(dataframe),
        'general_ira': general_ira(dataframe),
        'active_students': students[students.FORMA_EVASAO == EvasionForm.EF_ATIVO].shape[0],
        'graduated_students': students[students.FORMA_EVASAO == EvasionForm.EF_FORMATURA].shape[0],
    }

    save_json(path+'/degree.json', data)

    for ind, hist in dataframe.groupby('MATR_ALUNO'):
        generate_student_data(path+'students/{}.json'.format(ind), hist)



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

def generate_student_data(path, dataframe):
    ensure_path_exists(os.path.dirname(path))

    data = dict(dataframe.iloc[0][['MATR_ALUNO', 'NOME_ALUNO', 'SEXO', 'FORMA_INGRESSO', 'FORMA_EVASAO', 'ANO_INGRESSO',
                                'SEMESTRE_INGRESSO', 'ANO_EVASAO', 'SEMESTRE_EVASAO']])

    data.update({
        'ira': dataframe[dataframe.SITUACAO.isin(Situation.SITUATION_AFFECT_IRA)].MEDIA_FINAL.mean(),
        'completas': dataframe[dataframe.SITUACAO.isin(Situation.SITUATION_PASS)].shape[0],
        'tentativas': dataframe[dataframe.SITUACAO.isin(Situation.SITUATION_COURSED)].shape[0],
        'semestres': [process_semestre(per, dataframe[dataframe.PERIODO == per]) for per in sorted(dataframe.PERIODO.unique())],
        'historico': historico(dataframe)
    })

    save_json(path, data)


def generate_student_data_old(path, dataframe):
    print(aluno_turmas(dataframe))
    print(indice_aprovacao_semestral(dataframe))
    print("2007/1" in ira_por_quantidade_disciplinas(dataframe)["GRR20066955"])
    print(ira_semestra(dataframe)["GRR20079775"])
    aluno_turmas(dataframe)
    indice_aprovacao_semestral(dataframe)
    ira_por_quantidade_disciplinas(dataframe)
    ira_semestra(dataframe)
    periodo_pretendido(dataframe)
    print(periodo_real(dataframe))
    print(posicao_turmaIngresso_semestral(dataframe))
    print(listagem_evasao(dataframe))
    pass

def generate_student_list(path):
    pass

def generate_admission_data(path):
    pass

def generate_admission_list(path):
    pass

def generate_course_data(path):
    pass

def generate_course_general_data(path):
    pass
