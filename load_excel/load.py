#!/usr/bin/python3


'''
rodar do diretório adega, não do load_excel


'''

import re
import os
import sys
import pandas as pd

from glob import glob
from json import load as json_load

import django

sys.path.append(os.getcwd())

print(os.getcwd())

os.environ["DJANGO_SETTINGS_MODULE"] = "adega.settings"
django.setup()


from curso.models import *
from student.models import *
from disciplina.models import *
from turmaIngresso.models import *
from turma.models import *


hist = pd.read_excel('load_excel/relatorios/historico.xls', 'Planilha1')
matr = pd.read_excel('load_excel/relatorios/matricula.xls', 'Planilha1')

validos = set(hist.MATR_ALUNO.values)

bcc = Curso.objects.create(codigo='21A', ano_relatorio=2016,
                           semestre_relatorio=2, nome="Ciência da Computação")


g2007 = Grade.objects.create(curso=bcc, ano_inicio=2007)
g2011 = Grade.objects.create(curso=bcc, ano_inicio=2011)

with open('load_excel/data/bcc/grade2007.json') as f:
    g2007_data = json_load(f)

with open('load_excel/data/bcc/grade2011.json') as f:
    g2011_data = json_load(f)


for obr in g2007_data:
    d = Disciplina()

    d.codigo = obr['codigo']
    d.nome = obr['nome']
    d.carga_horaria = obr['carga_horaria']
    d.creditos = obr['creditos']

    d.save()

    dg = DisciplinaGrade()
    dg.grade = g2007
    dg.disciplina = d

    if 'periodo' in obr:
        dg.periodo = obr['periodo']
        
    dg.tipo_disciplina = obr['tipo']

    dg.save()




for obr in g2011_data:

    try:
        d = Disciplina.objects.get(codigo=obr['codigo'])
    except Disciplina.DoesNotExist:
        d = Disciplina()

        d.codigo = obr['codigo']
        d.nome = obr['nome']
        d.carga_horaria = obr['carga_horaria']
        d.creditos = obr['creditos']

        d.save()

    dg = DisciplinaGrade()
    dg.grade = g2011
    dg.disciplina = d
    
    if 'periodo' in obr:
        dg.periodo = obr['periodo']
        
    dg.tipo_disciplina = obr['tipo']

    dg.save()
    


for _, student in matr.iterrows():
    if student['MATR_ALUNO'] not in validos:
        continue

    s = Student()
    
    s.grr = student['MATR_ALUNO']
    s.name = student['NOME_PESSOA']
    
    s.forma_evasao = student['FORMA_EVASAO']
    
    grade = g2011
    
    if type(student['PERIODO_EVASAO']) == str:
        r = re.search('(?P<ano>\d*)/(?P<semestre>\d)', student['PERIODO_EVASAO'])
        
        if r is None:
            continue
        
        ano, semestre = int(r.group('ano')), int(r.group('semestre'))
        
        s.ano_evasao = ano
        s.semestre_evasao = semestre
        
        if ano < 2011:
            grade = g2007
        
    r = re.search('(?P<ano>\d*)/(?P<semestre>\d)', student['PERIODO_INGRESSO'])
    ano, semestre = int(r.group('ano')), int(r.group('semestre'))
    
    t, _ = TurmaIngresso.objects.get_or_create(ano=ano, semestre=semestre, curso=bcc)
    
    s.turma_ingresso = t
    
    s.grade_atual = grade
    
    s.save()


sys.exit(0)

for _, data in hist.iterrows():
    
    student = Student.objects.get(grr=data['MATR_ALUNO'])
    disciplina = Disciplina.objects.get(codigo=data['COD_ATIV_CURRIC'])
    
    ano = data['ANO']
    
    try:
        semestre = int(data['PERIODO'][0])
    except:
        semestre = 1
    
    turma = Turma.objects.get_or_create(disciplina=disciplina, ano=ano, semestre=semestre)
    
    t = AlunoTurma()
    
    t.turma = turma
    t.student = student
    
    t.nota = data['MEDIA_FINAL']
    
    t.situacao = data['SITUACAO']
    
    t.save()
    

    

