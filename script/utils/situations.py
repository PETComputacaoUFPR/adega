# == Admission Form == #
class AdmissionType:
    AT_DESCONHECIDO = 0
    AT_VESTIBULAR = 1
    AT_ENEM = 2
    AT_PROVAR = 3
    AT_REOPCAO = 4
    AT_TRANSFERENCIA_EX_OFICIO = 5
    AT_APROVEITAMENTO_CURSO = 6
    AT_MOBILIDADE = 7
    AT_REINTEGRACAO = 8
    AT_OUTROS = 100

    ADMISSION_FORM = (
        (AT_DESCONHECIDO, 'Desconhecido'),
        (AT_VESTIBULAR, 'Vestibular'),
        (AT_ENEM, 'ENEM'),
        (AT_PROVAR, 'PROVAR'),
        (AT_REOPCAO, 'Reopção de curso'),
        (AT_TRANSFERENCIA_EX_OFICIO, 'Transferência por ex-ofício'),
        (AT_APROVEITAMENTO_CURSO, 'Aproveitamento de curso'),
        (AT_MOBILIDADE, 'Mobilidade Acadêmica'),
        (AT_REINTEGRACAO, 'Reintegração'),
        (AT_OUTROS, 'Outro'),
    )

# == Evasion Form == #
class EvasionForm:
    EF_DESCONHECIDO = 0
    EF_ATIVO = 1
    EF_FORMATURA = 2
    EF_ABANDONO = 3
    EF_DESISTENCIA_VESTIBULAR = 4
    EF_CANCELAMENTO = 5
    EF_NAO_CONFIRMACAO_VAGA = 6
    EF_NOVO_VESTIBULAR = 7
    EF_TRANSFERENCIA_EXTERNA = 8
    EF_REOPCAO = 9
    EF_DESISTENCIA = 10
    EF_JUBILAMENTO = 11
    EF_OUTROS = 100

    EVASION_FORM = (
        (EF_DESCONHECIDO, 'Desconhecido'),
        (EF_ATIVO, 'Ativo'),
        (EF_FORMATURA, 'Formado'),
        (EF_ABANDONO, 'Abandono'),
        (EF_DESISTENCIA_VESTIBULAR, 'Desistencia vestibular'),
        (EF_CANCELAMENTO, 'Cancelamento'),
        (EF_NAO_CONFIRMACAO_VAGA, 'Não confirmação de vaga'),
        (EF_NOVO_VESTIBULAR, 'Novo vestibular'),
        (EF_TRANSFERENCIA_EXTERNA, 'Transferência externa'),
        (EF_REOPCAO, 'Reopção de curso'),
        (EF_DESISTENCIA, 'Desistência'),
        (EF_JUBILAMENTO, 'Jubilado'),
        (EF_OUTROS, 'Outros'),
    )

# == Situation Courses == #
class Situation:
    SIT_DESCONHECIDA = 0

    SIT_APROVADO = 1
    SIT_REPROVADO = 2
    SIT_MATRICULA = 3
    
    SIT_REPROVADO_FREQ = 4
    SIT_EQUIVALENCIA = 5
    SIT_CANCELADO = 6

    SIT_DISPENSA_COM_NOTA = 7
    SIT_DISPENSA_SEM_NOTA = 8

    SIT_CONHECIMENTO_APROVADO = 9
    SIT_CONHECIMENTO_REPROVADO = 10

    SIT_TRANCAMENTO_TOTAL = 11
    SIT_TRANCAMENTO_ADMINISTRATIVO = 12
    SIT_REPROVADO_SEM_NOTA = 13
    SIT_HORAS = 13

    SIT_OUTROS = 100

    SITUATIONS = (
        (SIT_DESCONHECIDA, 'Desconhecido'),
        (SIT_APROVADO, 'Aprovado'),
        (SIT_REPROVADO, 'Reprovado por nota'),
        (SIT_MATRICULA, 'Matrícula'),
        (SIT_REPROVADO_FREQ, 'Reprovado por Frequência'),
        (SIT_EQUIVALENCIA, 'Equivalência de Disciplina'),
        (SIT_CANCELADO, 'Cancelado'),

        (SIT_DISPENSA_COM_NOTA, 'Dispensa de Disciplinas (com nota)'),
        (SIT_DISPENSA_SEM_NOTA, 'Dispensa de Disciplinas (sem nota)'),
        (SIT_CONHECIMENTO_APROVADO, 'Aprov Conhecimento'),

        (SIT_CONHECIMENTO_REPROVADO, 'Reprov Conhecimento'),
        (SIT_TRANCAMENTO_TOTAL, 'Trancamento Total'),
        (SIT_TRANCAMENTO_ADMINISTRATIVO, 'Trancamento Administrativo'),
        (SIT_REPROVADO_SEM_NOTA, 'Reprovado sem nota'),

        (SIT_HORAS, 'Horas'),

        (SIT_OUTROS, 'Outro'),
    )

    SITUATION_AFFECT_IRA = (
        SIT_APROVADO,
        SIT_REPROVADO,
        SIT_REPROVADO_FREQ,
        SIT_DISPENSA_COM_NOTA,
        SIT_CONHECIMENTO_APROVADO,
        SIT_CONHECIMENTO_REPROVADO
    )

    SITUATION_PASS = (
        SIT_APROVADO,
        SIT_CONHECIMENTO_APROVADO,
        SIT_DISPENSA_COM_NOTA
    )

    SITUATION_FAIL = (
        SIT_REPROVADO,
        SIT_REPROVADO_FREQ,
        SIT_CONHECIMENTO_REPROVADO
    )
