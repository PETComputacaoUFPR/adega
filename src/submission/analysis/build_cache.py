from submission.analysis.conversor_de_dados_adega.utils.utils import save_json, ensure_path_exists
from submission.analysis.conversor_de_dados_adega.utils.situations import *
from submission.analysis.analysis.degree_analysis import *
from submission.analysis.analysis.student_analysis import *
from submission.analysis.analysis.course_analysis import Course

from submission.analysis.analysis.admission_analysis import Admission
from submission.analysis.analysis.admission_analysis import media_ira_turma_ingresso
from submission.analysis.analysis.admission_analysis import desvio_padrao_turma_ingresso
from submission.analysis.analysis.admission_analysis import students_per_semester
from submission.analysis.analysis.admission_analysis import admission_class_ira_per_semester
from submission.analysis.analysis.admission_analysis import evasion_per_semester


from submission.analysis.analysis.cepe9615_analysis import *

from student.grid import DegreeGrid

from collections import defaultdict

try:
    to_unicode = unicode
except NameError:
    to_unicode = str


student_analysis = None

CURRENT_YEAR = 2016
CURRENT_SEMESTER = 1

def build_cache(dataframe, path, current_year = CURRENT_YEAR,
                current_semester = CURRENT_SEMESTER):
    #   os.chdir("../src")


    ensure_path_exists(path)

    dg = DegreeGrid(DegreeGrid.bcc_grid_2011)
    student_analysis = StudentAnalysis(dataframe, current_year,
                                       current_semester, dg)

    for cod, df in dataframe.groupby('COD_CURSO'):
        path = path + '/'
        generate_degree_data(path, df, student_analysis)
        generate_student_data(path + 'students/', df, student_analysis)
        generate_admission_data(path + 'admissions/', df, student_analysis)
        generate_course_data(path + 'courses/',current_year, dataframe)
        generate_cepe_data(path, df)


def generate_cepe_data(path, df):
    cepe_dict = {}
    cepe_dict["student_fails_course"] = student_fails_course(df)
    cepe_dict["student_fails_2_courses"] = student_fails_2_courses(df)
    cepe_dict["fails_semester"] = fails_semester(df)
    cepe_dict["fails_by_freq_semester"] = fails_by_freq_semester(df)
    cepe_dict["fails_by_freq"] = fails_by_freq(df)
    save_json(path + "cepe9615.json", cepe_dict)


def generate_degree_data(path, dataframe, student_analysis):
    ensure_path_exists(path)

    build_degree_json(path, dataframe, student_analysis)


def process_semestre(per, df):
    ira = df[df.SITUACAO.isin(
        Situation.SITUATION_AFFECT_IRA)].MEDIA_FINAL.mean()
    completas = df[df.SITUACAO.isin(Situation.SITUATION_PASS)].shape[0]
    tentativas = df[df.SITUACAO.isin(Situation.SITUATION_COURSED)].shape[0]

    return {
        'semestre': per,
        'ira': ira,
        'completas': completas,
        'tentativas': tentativas,
        'aprovacao': completas / tentativas if tentativas else 0,
        'ira_por_quantidade_disciplinas': ira / tentativas if tentativas else 0
    }


def generate_student_data(path, dataframe, student_analysis):
    student_data = defaultdict(dict)
    all_grrs = list(dataframe["MATR_ALUNO"].drop_duplicates())
    for x in all_grrs:
        student_data[x] = dict()

    analysis = [
        # tuple that contains in the first element the function that returns a
        # dictionary with {"GRR": value} and in the second position the name
        # that this analysis will have in json

        (student_analysis.posicao_turmaIngresso_semestral(),
         "posicao_turmaIngresso_semestral"),

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
        save_json(path + x + ".json", student_data[x])

    files_list = [
        EvasionForm.EF_ABANDONO,
        EvasionForm.EF_DESISTENCIA,
        EvasionForm.EF_FORMATURA,
        EvasionForm.EF_ATIVO,
        EvasionForm.EF_OUTROS
    ]

    list_situations = student_analysis.list_students_situation()
    for fl in files_list:
        list_name = EvasionForm.code_to_str(int(fl))
        list_content = {"description_name":"", "description_value":""}
        if(fl in list_situations):
            list_content = list_situations[fl]
        save_json(path + "list/" + list_name + ".json", list_content)

    # TODO: Check if all students receive analysis

    # All students
    list_phases = student_analysis.list_students_phases()
    for phase_name in list_phases:
        list_content = list_phases[phase_name]
        save_json(path + "list/" + phase_name + ".json", list_content)

    # Only students without evasion
    list_phases = student_analysis.list_students_phases(only_actives=True)
    for phase_name in list_phases:
        list_content = list_phases[phase_name]
        save_json(path + "list/" + phase_name + ".json", list_content)

def generate_student_list(path):
    pass


def generate_admission_data(path, df, student_analysis):

    listagem = []
    a = Admission(df)
    a.build_analysis()
    admissions = a.build_cache()

    for i in admissions:
        save_json(path + str(i["ano"]) + "/" + str(i["semestre"]) + ".json", i)

    evasion_count = a.build_cache_evasion_count()
    analises = [
        ("ira", media_ira_turma_ingresso(df, student_analysis)),
        ("std", desvio_padrao_turma_ingresso(df, student_analysis)),
        ("ira_per_semester", admission_class_ira_per_semester(df)),
        ("evasion_per_semester", evasion_per_semester(df)),
        ("students_per_semester", students_per_semester(df)),
        ("quantidade_alunos", evasion_count["quantidade_alunos"]),
        ("abandono", evasion_count["abandono"]),
        ("ativos", evasion_count["ativos"]),
        ("formatura", evasion_count["formatura"]),
        ("alunos_evadidos", evasion_count["alunos_evadidos"]),
        ("outras_formas_evasao", evasion_count["outras_formas_evasao"])
    ]
    # cria um dicionario com as analises para cada turma
    turmas = defaultdict(dict)
    for a in analises:
        for x in a[1]:
            valor = a[1][x]
            x = (str(x[0]),  str(x[1]))
            turmas[x][a[0]] = valor

    listagem = []

    for t in turmas:
        resumo_turma = {
            "ano": t[0],
            "semestre": t[1]
        }

        for analise in turmas[t]:
            resumo_turma[analise] = turmas[t][analise]

        listagem.append(resumo_turma)

    save_json(path + "lista_turma_ingresso.json", listagem)


def generate_admission_list(path, df):
    pass


def generate_course_data(path, current_year, df):
    course = Course(current_year,df)
    course.build_analysis()
    courses = course.build_general_course()
    save_json(path + "disciplinas.json", courses)
    course_list = course.build_course()
    for i in course_list:
        save_json(path + i["disciplina_codigo"] + ".json", i)
