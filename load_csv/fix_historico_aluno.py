#!/usr/bin/env python
# *-* coding:utf-8

from __future__ import print_function
import pandas as pd
import sys


def preenhce_situacao_limpa_media_credito(row):
    if row['MEDIA_CREDITO'] != 'A':
        row['SITUACAO_CURRICULO'] = row['MEDIA_CREDITO']
        row['MEDIA_CREDITO'] = ''
    return row


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


PATH = sys.argv[1]
if not PATH:
    eprint('Erro: Passe o caminho do relatório do historico dos alunos como parametro')

df = pd.read_csv(PATH)
# shifta DESCR_ESTRUTURA e ID_ESTRUTURA_CUR uma coluna para direita
df = df.rename(columns={'DESCR_ESTRUTURA': 'OLD_DESCR_ESTRUTURA'})
df = df.rename(columns={'ID_ESTRUTURA_CUR': 'DESCR_ESTRUTURA'})
df = df.rename(columns={'ID_NOTA': 'ID_ESTRUTURA_CUR'})
df['ID_NOTA'] = pd.Series()

df = df.apply(preenhce_situacao_limpa_media_credito, axis=1)

df.to_csv(sys.stdout, sep=',', encoding='utf-8')
