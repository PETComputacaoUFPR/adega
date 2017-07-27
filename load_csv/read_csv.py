#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function
import sys
import os
import django
import pandas as pd

sys.path.append("..")
os.environ["DJANGO_SETTINGS_MODULE"] = "adega.settings"
django.setup()

from django.db import models
from student.models import *
from curso.models import *
from turmaIngresso.models import *
from disciplina.models import *
from turma.models import *
from student.analysis import calcular_ira
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

DIR_RELATORIOS = "../relatorios/"
CAMINHO_RELATORIO_DISCIPLINAS = DIR_RELATORIOS + "11.02.01.99.06-MUDA.csv"
CAMINHO_RELATORIO_MATRICULA = DIR_RELATORIOS + "11.02.04.99.43-MUDA.csv"
CAMINHO_RELATORIO_HISTORICOS = DIR_RELATORIOS + "11.02.05.99.33-historico-ira-curso-MUDA.csv"

"""
--------------------------------EXCEPTIONS--------------------------------

"""


class AlunoNaoExiste(Exception):
    pass


class DisciplinaNaoExiste(Exception):
    pass


class NenhumCursoEncontrado(Exception):
    pass


class NenhumaGradeEncontrada(Exception):
    pass


class GradeNaoEncontrada(Exception):
    pass


class NenhumaDisciplinaEncontrada(Exception):
    pass


_students = set()

m_students = dict()


"""
---------------------------------------------------------------------------
"""


# printa na saída de erros
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


"""
-------------------------FUNÇÕES LEITURA DOS RELATORIOS--------------------
"""


# todo: tratar exceptions
def ler_relatorio_disciplinas(listaDisciplinas):
    # TODO: validar se existe codigo do curso
    cursos_df = listaDisciplinas.drop_duplicates(subset=['COD_CURSO'])

    if cursos_df.empty:
        raise NenhumCursoEncontrado()

    # Pega o curso do banco de dados, caso ele não exista cria
    curso, curso_created = Curso.objects.get_or_create(codigo=cursos_df['COD_CURSO'][0],
                                                       nome=cursos_df['NOME_UNIDADE'][0])
    if curso_created:
        # grade criada, pois não temos todas as grades e queremos manter uma relação entre as disciplinas e o curso
        grade_fake = Grade(ano_inicio=1000,
                           curso=curso)
        grade_fake.save()

    # Agrupa os relatório pela versões da grade
    grades_df = listaDisciplinas[listaDisciplinas.COD_CURSO == curso.codigo].drop_duplicates(subset=['NUM_VERSAO'])

    if grades_df.empty:
        raise NenhumaGradeEncontrada()

    # Percorre as grades do curso
    for index, row in grades_df.iterrows():
        # Pega a grade do banco de dados, caso ela ainda não exista cria
        grade, grade_created = Grade.objects.get_or_create(curso=curso,
                                                           ano_inicio=row['NUM_VERSAO'])
        ler_disciplinas_grade(listaDisciplinas, grade)
    return curso


def ler_disciplinas_grade(listaDisciplinas, grade):
    # Seleciona as linahs que são do curso da grade e da versão da grade
    disciplinas_df = listaDisciplinas[(listaDisciplinas.COD_CURSO == grade.curso.codigo)
                                      & (listaDisciplinas.NUM_VERSAO == grade.ano_inicio)].drop_duplicates(
        subset=['COD_DISCIPLINA'])

    if disciplinas_df.empty:
        raise NenhumaDisciplinaEncontrada()
    for index, row in disciplinas_df.iterrows():
        # Pega a disciplina no banco de dados, caso ela não exista, cria
        disciplina, disciplina_created = Disciplina.objects.get_or_create(
            codigo=row['COD_DISCIPLINA'], defaults={
                'nome': row['NOME_DISCIPLINA'],
                'carga_horaria': row['CH_TOTAL'],
            })
        # Caso a disciplina não exista ainda no banco de dados também cria a relação com a grade
        if disciplina_created:
            dg = DisciplinaGrade(grade=grade,
                                 disciplina=disciplina,
                                 periodo=row['PERIODO_IDEAL'],
                                 tipo_disciplina=row['TIPO_DISCIPLINA'])
            dg.save()


def ler_relatorio_matriculas(matricula_aluno_df, curso):
    # Muda valores que estão com NaN para None
    matricula_aluno_df = matricula_aluno_df.where((pd.notnull(matricula_aluno_df)), None)
    students = []

    # Seleciona os alunos que são do curso
    curso_df = matricula_aluno_df[matricula_aluno_df.COD_CURSO == curso.codigo]

    # Agrupa os alunos pela versão da grade que está
    grouped_grade_df = curso_df.groupby('VERSAO')

    # Percorre as grades
    for ano_grade, grade_df in grouped_grade_df:

        try:
            grade = curso.grade_set.get(ano_inicio=ano_grade)
        except ObjectDoesNotExist as ex:
            # raise GradeNaoEncontrada()
            eprint("GradeNaoEncontrada: versao:{0}".format(ano_grade))
            continue;
        # TODO: Remover o filtro da data de ingresso no formato certo e adicionar validação
        ti_df = curso_df[
            matricula_aluno_df.DT_INGRESSO.str.contains("^(0[1-9]|[12][0-9]|3[01])[/](0[1-9]|1[012])[/](\d){4}$",
                                                        na=False)]

        ti_df['DT_INGRESSO'] = pd.to_datetime(ti_df['DT_INGRESSO'], format="%d/%m/%Y")
        ti_df['ANO'] = ti_df['DT_INGRESSO'].dt.year
        ti_df['SEMESTRE'] = ti_df['DT_INGRESSO'].apply(lambda d: 1 if d.month <= 6 else 2)

        grouped_ti_df = ti_df.groupby(['ANO', 'SEMESTRE'])

        for names, group in grouped_ti_df:
            ti, created_ti = TurmaIngresso.objects.get_or_create(ano=names[0], semestre=names[1], curso=curso)
            for index, student_row in group.iterrows():
                # TODO: Descobrir o que fazer com evasao anual
                # anual e dado invalido é tratada como primeiro semestre por enquanto
                semestre_evasao = None
                if student_row['PERIODO_EVASAO'] in SEMESTRE:
                    semestre_evasao = SEMESTRE[student_row['PERIODO_EVASAO']]
                elif student_row['PERIODO_EVASAO'] == "Anual":
                    semestre_evasao = 1
                    
                if student_row['MATRICULA'][3:] not in _students:
                    _students.add(student_row['MATRICULA'][3:])

                    
                    student, created_student = Student.objects.get_or_create(grr=student_row['MATRICULA'][3:],
                                                                             defaults={'name': student_row['ALUNO'],
                                                                                       'ira': 0,
                                                                                       'forma_evasao': student_row[
                                                                                           'FORMA_EVASAO'],
                                                                                       'ano_evasao': student_row[
                                                                                           'ANO_EVASAO'],
                                                                                       'semestre_evasao': semestre_evasao,
                                                                                       'turma_ingresso': ti,
                                                                                       'grade_atual': grade
                                                                                       })
                                                                                       
                    m_students[student_row['MATRICULA'][3:]] = student
                    
                    students.append(student)
    return students



def ler_historico_aluno(historico_df, curso):
    disciplinas_gdf = historico_df.groupby('COD_ATIV_CURRIC')
    grade_fake = curso.grade_set.get(ano_inicio=1000)

    # inicializa data relatorio com nulo, para ser preenchida durante a leitura
    curso.ano_relatorio = 0
    curso.semestre_relatorio = 0

    for codigo_disciplina, disciplina_df in disciplinas_gdf:
        try:
            disciplina = Disciplina.objects.get(codigo=codigo_disciplina)
        except ObjectDoesNotExist:
            primeira_linha = disciplina_df.iloc[0]
            descr_estrutura = primeira_linha['DESCR_ESTRUTURA']
            carga_horaria = primeira_linha['CH_TOTAL']
            nome_disciplina = primeira_linha['NOME_ATIV_CURRIC']

            if descr_estrutura == "Disciplinas de outros cursos":
                disciplina = Disciplina(codigo=codigo_disciplina,
                                        nome=nome_disciplina,
                                        carga_horaria=carga_horaria)
                disciplina.save()

            # FIXME: REMOVER GRADE FAKE DEPOIS DE OBTER DE TER CERTEZA QUE TEMOS TODOS OS CURRICULOS
            elif descr_estrutura == "Discipl. de outros currículos do curso":
                disciplina = Disciplina(codigo=codigo_disciplina,
                                        nome=nome_disciplina,
                                        carga_horaria=carga_horaria)
                disciplina.save()

                dg = DisciplinaGrade(grade=grade_fake,
                                     disciplina=disciplina,
                                     periodo=1,
                                     tipo_disciplina=descr_estrutura)
                dg.save()

            # TODO:O que fazer com as atividades formativas? Elas não são disciplinas, porém o que fazer com elas? obs: existem poucos registros delas no relatório, talvez elas não devam contar nele mesmo
            elif descr_estrutura == "Atividades Formativas Complementares":
                eprint("Atividade Formativa Encontrada: codigo={0}".format(codigo_disciplina))
                continue
            else:
                try:
                    raise DisciplinaNaoExiste("DisciplinaNaoExiste: codigo={0}".format(codigo_disciplina))
                except DisciplinaNaoExiste as ex:
                    eprint(ex)
                    continue

        # FIXME: Adicionar mais uma chave no group by para separar as turmas do mesmo ano e semestre(talvez sigla?)
        turmas_gdf = disciplina_df.groupby(['ANO', 'PERIODO'])
        # periodo do relatório na verdade é o semestre(1 ou 2)
        for ano_periodo, turma_df in turmas_gdf:
            if ano_periodo[1] not in SEMESTRE:
                eprint(
                    "PERIODO INVALIDO: cod_disciplina={0} ano={1} periodo:{2}".format(codigo_disciplina, ano_periodo[0],
                                                                                      ano_periodo[1]))
                continue
            ano = ano_periodo[0]
            semestre = SEMESTRE[ano_periodo[1]]
            """"
            Pega a maior data do historico para ser a data que as informações do relatório são válidas
            """
            if ano > curso.ano_relatorio:
                curso.ano_relatorio = ano
                curso.semestre_relatorio = semestre
            elif ano == curso.semestre_relatorio:
                if semestre > curso.semestre_relatorio:
                    curso.semestre_relatorio = semestre

            turma, created_turma = Turma.objects.get_or_create(disciplina=disciplina,
                                                               ano=ano,
                                                               semestre=semestre
                                                               )
            # TODO: validar se existe estudantes iguais na turma
            for index, student_row in turma_df.iterrows():
                grr = student_row['MATR_ALUNO'][3:]
                
                if grr not in _students:
                    try:
                        raise AlunoNaoExiste("AlunoNaoExiste: GRR={0}".format(grr))
                    except AlunoNaoExiste as ex:
                        eprint(ex)
                        continue
                        
                student = m_students[grr]

                # TODO: Verficar se o valor 9999 é o valor real do relatório, ou foi atribuido na criptografia do relatório
                nota = 0 if student_row['MEDIA_FINAL'] == 9999 else student_row['MEDIA_FINAL']

                # Não adianta só checar o created_turma p/ saber se precisa ou não criar o aluno_turma, pois o relatório anteriormente enviado pode não conter o aluno ainda, por exemplo antes do reajuste de matricula
                aluno_turma, create_aluno_turma = AlunoTurma.objects.get_or_create(
                    turma=turma, student=student, defaults={
                        'nota': nota,
                        'situacao': student_row['SITUACAO']
                    })
    # salva ano, semestre do relatório
    curso.save()


"""
--------------------------------------------------------------------------------
"""


def gerar():
    # ofertaDisciplina = pd.read_csv(DIR_RELATORIOS + "11.02.03.99.05-MUDA.csv")


    relatorio_disciplinas_df = pd.read_csv(CAMINHO_RELATORIO_DISCIPLINAS)
    print("ANALISANDO O RELATÓRIO DE DISCIPLINAS")
    curso = ler_relatorio_disciplinas(relatorio_disciplinas_df)

    print("ANALISANDO O RELATÓRIO DE MATRICULAS")
    relatorio_matriculas_df = pd.read_csv(CAMINHO_RELATORIO_MATRICULA)
    students = ler_relatorio_matriculas(relatorio_matriculas_df, curso)

    print("ANALISANDO O RELATÓRIO DOS HISTÓRICOS")
    relatorio_historicos_df = pd.read_csv(CAMINHO_RELATORIO_HISTORICOS)
    ler_historico_aluno(relatorio_historicos_df, curso)

    print("CALCULANDO IRAs")
    # Atribui ira para os alunos dos relatórios
    for student in students:
        student.ira = calcular_ira(student.alunoturma_set.all())
        student.save()


def apagar():
    AlunoTurma.objects.all().delete()
    Student.objects.all().delete()
    Turma.objects.all().delete()
    Disciplina.objects.all().delete()
    TurmaIngresso.objects.all().delete()
    Curso.objects.all().delete()


gerar()
# apagar()
