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
    u'Aprovado',
    u'Aprovado Adiantamento',
    u'Equivalência de Disciplinas',
    u'Aprovado Conhecimento',
)

SITUATION_CANCELLATION = ( # Situacoes de cancelamento
    u'Cancelado',
)

SITUATIONS_PASS_KNOWLEDGE = (
    u'Aprovado Conhecimento',
)

SITUATIONS_FAIL_KNOWLEDGE = (
    u'Reprovado Conhecimento',
)


SITUATION_NO_EVASION = ( # Situacoes nao evasao
    u'Sem evasão',
    u'Formatura',
    u'Reintegração',
)

SITUATION_EVASION_OTHERS = (
    u'Cancelamento a Pedido do Calouro',
    u'Cancelamento Pedido',
    u'Descumprimento Edital',
    u'Desistência',
    u'Desistência Vestibular',
    u'Falecimento',
    u'Jubilamento',
    u'Não Confirmação de Vaga',
    u'Novo Vestibular',
    u'Reopção',
    u'Término de Registro Temporário',
    u'Transferência Externa',
    u'Cancelamento Convênio',
    u'Cancelamento Judicial',
    u'Desistência PROVAR',
    u'Reintegração'
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

SITUATION_COURSES_VALID = (
    u'Reprovado por nota',
    u'Aprovado',
    u'Reprovado por Frequência',
    u'Reprovado sem nota',
    u'Equivalência de Disciplina',
    u'Aprovado Conhecimento',
    u'Reprovado Conhecimento',
    u'Aprovado Adiantamento',
    u'Horas',
    u'Dispensa de Disciplinas (com nota)',
    u'Dispensa de Disciplinas (sem nota))',
    u'Matrícula',
)

SITUATION_COURSES_LOCKED = (
    u'Cancelado',
    u'Trancamento Total',
    u'Trancamento Administrativo',
)

SITUATION_COURSES_VALID_GRADE = (
    u'Reprovado por nota',
    u'Aprovado',
    u'Reprovado por Frequência',
    u'Reprovado sem nota',
    u'Equivalência de Disciplina',
    u'Aprovado Conhecimento',
    u'Reprovado Conhecimento',
    u'Aprovado Adiantamento',
    u'Horas',
    u'Dispensa de Disciplinas (com nota)',
    u'Dispensa de Disciplinas (sem nota))',
)

def difference_between_semesters(year_start, semester_start, year_end, semester_end):
    return 2 * (year_end - year_start) + (semester_end - semester_start) + 1

def merge_dicts(keys, *args):
    dict_out = {}
    size = len(args)

    for key, value in args[0].items():
        values = []
        values.append(value)
        for i in range(1, size):
            values.append(args[i][key] if key in args[i] else None)

        dict_out[key] = {keys[i]: values[i] for i in range(0, size)}

    return dict_out
