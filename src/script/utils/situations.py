# -*- coding: utf-8 -*-
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
    EF_DESCUMPRIMENTO_EDITAL = 12
    EF_FALECIMENTO = 13
    EF_TERMINO_REG_TEMP = 14
    EF_REINTEGRACAO = 15
    EF_OUTROS = 100

    EVASION_FORM = (
        (EF_DESCONHECIDO, 'Desconhecido'),
        (EF_ATIVO, 'Sem evasão'),
        (EF_FORMATURA, 'Formatura'),
        (EF_ABANDONO, 'Abandono'),
        (EF_DESISTENCIA_VESTIBULAR, 'Desistência Vestibular'),
        (EF_CANCELAMENTO, 'Cancelamento'),
        (EF_NAO_CONFIRMACAO_VAGA, 'Não Confirmação de Vaga'),
        (EF_NOVO_VESTIBULAR, 'Novo Vestibular'),
        (EF_TRANSFERENCIA_EXTERNA, 'Transferência Externa'),
        (EF_REOPCAO, 'Reopção'),
        (EF_DESISTENCIA, 'Desistência'),
        (EF_JUBILAMENTO, 'Jubilamento'),
        (EF_DESCUMPRIMENTO_EDITAL, 'Descumprimento Edital'),
        (EF_FALECIMENTO, 'Falecimento'),
        (EF_TERMINO_REG_TEMP, 'Término de Registro Temporário'),
        (EF_REINTEGRACAO, 'Reintegração'),
        (EF_OUTROS, 'Outro'),
    )

    @staticmethod
    def code_to_str(code):
        for ef in EvasionForm.EVASION_FORM:
            if(ef[0] == code):
                return ef[1].replace("'","").replace("\"","")
        return ""
    
    @staticmethod
    def str_to_code(str):
        for ef in EvasionForm.EVASION_FORM:
            if(ef[1] == str):
                return ef[0]
        return -1

# == Situation Courses == #
#note:  os valores da coluna media_final não são confiavel, situation como
# reprovacao,reprovacao_freq,dispensa_com_nota aparecem em algumas linha como
# 9999, o valor 9999 é o valor definido pelo sie para ser o 'null' na tabela
# .33, na tabela .18 o 'null' é o zero e não ocorre problema de calculo de
# nota/ira  
# orientaçao: verificar se media_final é maior que 100 se sim atribua 0 se nao
# atribua media_final


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
    SIT_HORAS = 14

    SIT_APROV_ADIANTAMENTO = 15
    SIT_INCOMPLETO = 16
    
    SIT_REPROVADO_ADIAN = 17

    SIT_OUTROS = 100

    SITUATIONS = (
        (SIT_DESCONHECIDA, 'Desconhecido'),
        (SIT_APROVADO, 'Aprovado'),
        (SIT_REPROVADO, 'Reprovado por nota'),
        (SIT_MATRICULA, 'Matrícula'),
        (SIT_REPROVADO_FREQ, 'Reprovado por Frequência'),
        (SIT_REPROVADO_ADIAN, 'Reprov Adiantamento'),
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

        (SIT_APROV_ADIANTAMENTO, 'Aprov Adiantamento'),
        (SIT_INCOMPLETO, 'Incompleto'),
        (SIT_OUTROS, 'Outro'),
    )

    SITUATION_AFFECT_IRA = (
        SIT_APROVADO,
        SIT_REPROVADO,
        SIT_REPROVADO_FREQ,
        SIT_DISPENSA_COM_NOTA,
        SIT_CONHECIMENTO_APROVADO,
        SIT_REPROVADO_ADIAN,
        SIT_CONHECIMENTO_REPROVADO
    )

    SITUATION_PASS = (
        SIT_APROVADO,
        SIT_CONHECIMENTO_APROVADO,
        SIT_DISPENSA_COM_NOTA
    )

    SITUATION_KNOWLDGE = (
            SIT_CONHECIMENTO_APROVADO,
            SIT_CONHECIMENTO_REPROVADO
    )

    SITUATION_FAIL = (
        SIT_REPROVADO,
        SIT_REPROVADO_FREQ,
        SIT_REPROVADO_ADIAN,
        SIT_CONHECIMENTO_REPROVADO
    )

    """
    isso deve ser pra filtrar fora coisas que não são disciplinas cumpridas
    
    como "trancamento administrativo" e "horas"
    
    importante pra saber quantas matérias um aluno REALMENTE fez em um semestre
    """
    SITUATION_COURSED = (
        SIT_APROVADO,
        SIT_REPROVADO,
        SIT_REPROVADO_FREQ,
        SIT_DISPENSA_COM_NOTA,
        SIT_CONHECIMENTO_APROVADO,
        SIT_CONHECIMENTO_REPROVADO,
        SIT_REPROVADO_SEM_NOTA,
        SIT_INCOMPLETO,
            SIT_CANCELADO,
    )
