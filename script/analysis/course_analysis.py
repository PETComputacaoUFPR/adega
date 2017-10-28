# -*- coding: utf-8 -*-
import pandas as pd
import json
import numpy as np
import utils.situations

    with pd.option_context('display.max_rows', None, 'display.max_columns', 27):
        print(d)

# calcula as taxas
    c = matr[x['COD_ATIV_CURRIC']].values[0]
    return (x['counts'] / c)

# quantidade de matriculas
    return df.groupby(['COD_ATIV_CURRIC']).size()

    qnt_matr = counts_matr(df)  # quantidade de matriculas disciplina
    # conta quantas vezes os valores de 'SIGLA' se repete para cada disciplina
    diciplines = df.groupby(['COD_ATIV_CURRIC', 'SIGLA']
                             ).size().reset_index(name='counts')
    # adiciona mais uma coluna ao df disciplina com as taxas de cada valor de 'SIGLA'
    disciplines = diciplines.groupby(['COD_ATIV_CURRIC', 'SIGLA', 'counts']).apply(
        lambda x: func(x, qnt_matr)).reset_index(name='taxas gerais')
    Disciplines= disciplines['COD_ATIV_CURRIC'].drop_duplicates()
    for discipline in Disciplines:
        print(diciplines.discipline)
        # print(discipline)
    return disciplines

# quantidade de vezes cursadas ate obter a aprovacao
    qnt = df.groupby(['MATR_ALUNO', 'COD_ATIV_CURRIC']
                     ).size().reset_index(name='qnt_aprov')
    return qnt

    return df.groupby(['COD_ATIV_CURRIC', 'PERIODO', 'ANO']).size()

    ano = int(x['ANO'])
    periodo = x['PERIODO'].values[0]
    disciplina = x['COD_ATIV_CURRIC'].values[0]
    c = matr[disciplina, periodo, ano]
    return (x['counts_semestre'] / c)

    qnt_matr_semestre = matr_semestre(df)
    discipline_semestre = df.groupby(['COD_ATIV_CURRIC', 'PERIODO', 'ANO', 'SIGLA']).size(
    ).reset_index(name='counts_semestre')
    discipline_semestre = discipline_semestre.groupby(['COD_ATIV_CURRIC', 'PERIODO', 'ANO', 'SIGLA']).apply(lambda x: func_semestre(x,
                                                                                                                                    qnt_matr_semestre)).reset_index(name='taxas_semetrais')

    return discipline_semestre


    Analysis = analysis(df)
    Analysis_semestre = analysis_semestre(df)
    matr = counts_matr(df)
    matr_semes = matr_semestre(df)
