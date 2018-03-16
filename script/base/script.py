#!/usr/bin/env python3


import pandas as pd
import numpy as np
from random import choice, randrange, seed
from glob import glob


matriculas_semestrais = glob('1102049907_*.xls')

display_grrs = ('GRR20132413', 'GRR20123145', 'GRR20135427', 'GRR20132356', 'GRR20073965', 'GRR20142054')

seed(2315484613)


with open('nomes/f.txt') as fi:
    f = list(map(str.strip, fi.readlines()))
    
with open('nomes/m.txt') as fi:
    m = list(map(str.strip, fi.readlines()))
    
with open('nomes/s.txt') as fi:
    s = list(map(str.strip, fi.readlines()))



def gera_nome(sexo):
    return "{} {} {}".format(choice(m) if sexo == 'M' else choice(f),
                             choice(s), choice(s))
    

def gera_grr(grrs):
    gerados = set()
    
    result = []
    
    for grr in grrs:
        e = 'GRR{}{:0>4}'.format(grr[3:7], randrange(10000))
        
        while e in gerados:
            e = 'GRR{}{:0>4}'.format(grr[3:7], randrange(10000))
        
        result.append(e)
        gerados.add(e)
    
    return result



hist = pd.read_excel('1102059918.xls', 'Sheet1')
matr = pd.read_excel('1102049901.xls', 'Sheet1')

print('historico lines:', hist.shape[0])
print('matricula lines:', matr.shape[0])

def change_dt(s):
    return '01/01/{}'.format(s.split('/')[2])

vhist = hist.MATR_ALUNO.drop_duplicates()
vmatr = matr.MATR_ALUNO.drop_duplicates()

print('historico alunos:', vhist.shape[0])
print('matricula alunos:', vmatr.shape[0])

validos = set(vhist) & set(vmatr)

print('validos:',len(validos))



hist = hist[hist.MATR_ALUNO.isin(validos)]
matr = matr[matr.MATR_ALUNO.isin(validos)]

print('historico lines:', hist.shape[0])

mapper = matr[['MATR_ALUNO', 'NOME_PESSOA', 'DT_NASCIMENTO']].copy()



mapper['FAKE_GRR'] = gera_grr(mapper.MATR_ALUNO)


mapper['FAKE_NOME'] = matr.SEXO.apply(gera_nome)


matr['MATR_ALUNO'] = mapper['FAKE_GRR']
matr['NOME_PESSOA'] = mapper['FAKE_NOME']
matr['DT_NASCIMENTO'] = matr.DT_NASCIMENTO.apply(change_dt)


m_grr = dict(zip(mapper.MATR_ALUNO, mapper.FAKE_GRR))
m_nome = dict(zip(mapper.MATR_ALUNO, mapper.FAKE_NOME))

hist['NOME_PESSOA'] = hist.MATR_ALUNO.map(m_nome)
hist['MATR_ALUNO'] = hist.MATR_ALUNO.map(m_grr)


c = ['MATR_ALUNO', 'NOME_PESSOA', 'FAKE_GRR']

for _ , v in mapper.loc[mapper.MATR_ALUNO.isin(display_grrs), c].iterrows():
	print('{:>10}\t{:38}\t{:>10}'.format(*list(v)))

hist.sort_values('MATR_ALUNO').to_excel('historico.xls', 'Sheet1', index=False)
matr.sort_values('MATR_ALUNO').to_excel('matricula.xls', 'Sheet1', index=False)

mapper.to_excel('mapper.xls', 'Sheet1')


for rel in matriculas_semestrais:
    r = pd.read_excel(rel, 'Sheet1')
    
    r = r[r.MATR_ALUNO.isin(validos)]
    
    r['NOME_ALUNO'] = r.MATR_ALUNO.map(m_nome)
    r['MATR_ALUNO'] = r.MATR_ALUNO.map(m_grr)
    r['DT_NASCIMENTO'] = r.DT_NASCIMENTO.apply(change_dt)
    
    r.sort_values('MATR_ALUNO').to_excel('_'+rel, 'Sheet1', index=False)



