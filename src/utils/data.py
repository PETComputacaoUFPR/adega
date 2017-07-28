SITUATIONS_COURSE_COMPLETED = ( # Situacoes cursadas ate o fim
    u'Reprovado por nota',
    u'Aprovado',
    u'Aprovado Adiantamento',
    u'Reprovado por Frequência',
    u'Reprovado sem note',
)

SITUATIONS_FAILURE = ( # Situacoes reprovacao
    u'Reprovado por nota',
    u'Reprovado por Frequência',
    u'Reprovado sem nota',
)

SITUATION_CONCLUDED = ( # Situacoes concluidas
    u'Aprovado',
    u'Aprovado Adiantamento',
    u'Aprov Conhecimento',
    u'Aprovado Conhecimento',
    u'Dispensa de Disciplinas (com nota)',
    u'Dispensa de Disciplinas (sem nota)',
    u'Equivalência de Disciplina'
)

SITUATION_PASS = ( # Situacoes aprovacao
    u'Aprovado'
    u'Aprovado Adiantamento',
    u'Equivalência de Disciplinas',
    u'Aprovado Conhecimento',
)


SITUATION_NO_EVASION = ( # Situacoes nao evasao
    u'Sem evasão',
    u'Formatura',
    u'Reintegração',
)

SITUATION_LOCKING = ( # Situacoes trancamento
    u'Trancamento Total',
    u'Trancamento Administrativo'
)


SITUATION_AFFECT_IRA = ( # Situacoes contribuem para o ira
    u'Reprovado por nota',
    u'Aprovado',
    u'Reprovado por Frequência',
    u'Reprovado sem nota',
    u'Aprovado Adiantamento', # TODO: Descobrir se realmente contribui
)

SITUATION_FAILURE_COMPLETED = ( # Situacoes reprovacao cursada ate o fim
    u'Reprovado por nota',
    u'Reprovado por Frequência',
    u'Reprovado sem nota',
)

def difference_between_semesters(year_start, semester_start, year_end, semester_end):
    return 2 * (year_end - year_start) + (semester_end - year_end) + 1

def merge_dicts(dict1, dict2, dict3, keys):
    dict_out = {}
    for key, value in dict1.items():
        v2 = dict2[key] if key in dict2 else None
        v3 = dict3[key] if key in dict3 else None
        dict_out[key] = {keys[0]: value, keys[1]: v2, keys[2]: v3}

    return dict_out
