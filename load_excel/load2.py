#!/usr/bin/python3

import re
import os
import sys
import pandas as pd

from glob import glob
from json import load as json_load

import django

sys.path.append(os.getcwd())

os.environ["DJANGO_SETTINGS_MODULE"] = "adega.settings"
django.setup()


from curso.models import *
from student.models import *
from disciplina.models import *
from turmaIngresso.models import *
from turma.models import *


hist = pd.read_excel('load_excel/relatorios/historico.xls', 'Planilha1')

total = hist.shape[1]

  
     

def proccess(d):

    data = d[1]

    try:
        student = Student.objects.get(grr=data['MATR_ALUNO'])
        disciplina = Disciplina.objects.get(codigo=data['COD_ATIV_CURRIC'])
    except:
        return
    
    ano = data['ANO']
    
    try:
        semestre = int(data['PERIODO'][0])
    except:
        semestre = 1
    
    turma, _ = Turma.objects.get_or_create(disciplina=disciplina, ano=ano, semestre=semestre)
    
    t = AlunoTurma()
    
    t.turma = turma
    t.student = student
    
    t.nota = data['MEDIA_FINAL']
    
    t.situacao = data['DESCR_SITUACAO']
    
    t.save()
    
    
count = 0
total = hist.shape[0]

for i in hist.iterrows():
    proccess(i)
    
    if count % 100 == 0:
        print('{:>6} / {}'.format(count, total))
        
    count += 1
