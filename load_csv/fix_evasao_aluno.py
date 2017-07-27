#!/usr/bin/env python
# *-* coding:utf-8

from __future__ import print_function
import pandas as pd
import sys


def shift_evasao(row):
    if row['ANO_EVASAO'] in ("1o. Semestre", "2o. Semestre"):
        row['PERIODO_EVASAO'] = row['ANO_EVASAO']
        row['ANO_EVASAO'] = row['DT_SAIDA']
        row['DT_SAIDA'] = None
    return row


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


PATH = sys.argv[1]
if not PATH:
    eprint('Erro: Passe o caminho do relatório de matricula  dos alunos como parametro')

df = pd.read_csv(PATH)

df = df.apply(shift_evasao, axis=1)

df.to_csv(sys.stdout, sep=',', encoding='utf-8')
