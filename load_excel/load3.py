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

from student.analysis import SITUACOES_CONTRIBUEM_IRA


hist = pd.read_excel('load_excel/relatorios/historico.xls', 'Planilha1')



group = hist.groupby('MATR_ALUNO')

total = len(group)

for i, data in enumerate(group):

    index, data = data[0], data[1]
    
    try:
        aluno = Student.objects.get(grr=index)
    except:
        continue
    
    print("{:>5}/{}\t\t{}".format(i, total, index))
    
    ira = data[data.DESCR_SITUACAO.isin(SITUACOES_CONTRIBUEM_IRA)].MEDIA_FINAL.mean()
    
    aluno.ira = ira if pd.notnull(ira) else None 
    
    aluno.save()
    
    
    
