
from utils.situations import *

ANO_ATUAL = 2017
SEMESTRE_ATUAL = 2


def listagem_evasao(df):
    # ~ print(df["FORMA_EVASAO"].drop_duplicates())
    # ~ print(df)
    # ~ print(Situation.SITUATION_AFFECT_IRA)
    # ~ print(df)
    aux = df[df.FORMA_EVASAO != 1]
    print(aux)


# ~ print(aux.where(aux.SITUACAO != 1)["SITUACAO"])
# ~ print(df[df.SITUACAO.isin(Situation.SITUATION_AFFECT_IRA)])
# ~ print(df.where(df["SITUACAO"] in Situation.SITUATION_AFFECT_IRA))
# ~ aux = df.drop_duplicates(['MATR_ALUNO'], keep='last')
# ~ print(aux["FORMA_EVASAO"].drop_duplicates())

def average_ira(d):
    temp = d.dropna(subset=['MEDIA_FINAL'])
    temp = temp[temp['MEDIA_FINAL'] <= 100]
    if not temp.empty:
        # print(temp[['MEDIA_FINAL', 'CH_TOTAL']])
        aux = np.sum(temp['MEDIA_FINAL'] * temp['CH_TOTAL'])
        ch_total = np.sum(temp['CH_TOTAL']) * 100
        return (aux / ch_total)


def posicao_turmaIngresso_semestral(df):
    iras = ira_semestra(df)
    iraMax = {}
    for matr in iras:
        for semestreAno in iras[matr]:
            if not (semestreAno in iraMax):
                iraMax[semestreAno] = iras[matr][semestreAno]
            else:
                if (iras[matr][semestreAno] > iraMax[semestreAno]):
                    iraMax[semestreAno] = iras[matr][semestreAno]
    for matr in iras:
        for semestreAno in iras[matr]:
            iras[matr][semestreAno] /= iraMax[semestreAno]

    return iras


def periodo_real(df):
    aux = df.groupby(["MATR_ALUNO"])
    students = {}
    for x in aux:
        students[x[0]] = None
    return students


def periodo_pretendido(df):
    aux = df.groupby(["MATR_ALUNO", "ANO_INGRESSO", "SEMESTRE_INGRESSO"])
    students = {}
    for x in aux:
        print(x[0][0] + " : " + x[0][1] + " " + x[0][2])
        students[x[0][0]] = (ANO_ATUAL - int(x[0][1])) * 2 + SEMESTRE_ATUAL - int(x[0][2]) + 1
    return students


def ira_semestra(df):
    aux = ira_por_quantidade_disciplinas(df)
    for matr in aux:
        for periodo in aux[matr]:
            aux[matr][periodo] = aux[matr][periodo][0]
    return aux


def ira_por_quantidade_disciplinas(df):
    students = {}
    df = df.dropna(subset=["MEDIA_FINAL"])
    # ~ print(df["MATR_ALUNO"][178])
    # ~ print(df["NOME_ATIV_CURRIC"][178])
    # ~ print(df["PERIODO"][178])
    # ~ print(df["ANO"][178])
    # ~ print(df["SITUACAO"][178])

    total_students = len(df["MATR_ALUNO"])
    for i in range(total_students):
        matr = (df["MATR_ALUNO"][i])
        if (not (matr in students)):
            students[matr] = {}

        ano = str(int(df["ANO"][i]))
        semestre = str(df["PERIODO"][i])
        situacao = int(df["SITUACAO"][i])
        nota = float(df["MEDIA_FINAL"][i])
        media_credito = int(df["MEDIA_CREDITO"][i])

        if (situacao in Situation.SITUATION_AFFECT_IRA and media_credito != 0):

            if not (ano + "/" + semestre in students[matr]):
                students[matr][ano + "/" + semestre] = [0, 0]
            students[matr][ano + "/" + semestre][0] += nota
            students[matr][ano + "/" + semestre][1] += 1

    for matr in students:
        for periodo in students[matr]:
            if (students[matr][periodo][1] != 0):
                students[matr][periodo][0] /= students[matr][periodo][1] * 100
    return (students)


def indice_aprovacao_semestral(df):
    students = {}
    df = df.dropna(subset=['MEDIA_FINAL'])
    total_students = len(df["MATR_ALUNO"])
    for i in range(total_students):
        matr = (df["MATR_ALUNO"][i])
        if (not (matr in students)):
            students[matr] = {}

        ano = str(int(df["ANO"][i]))
        semestre = str(df["PERIODO"][i])
        situacao = int(df["SITUACAO"][i])

        if not (ano + "/" + semestre in students[matr]):
            students[matr][ano + "/" + semestre] = [0, 0]

        if situacao in Situation.SITUATION_PASS:
            students[matr][ano + "/" + semestre][0] += 1
            students[matr][ano + "/" + semestre][1] += 1
        if situacao in Situation.SITUATION_FAIL:
            students[matr][ano + "/" + semestre][1] += 1
    return (students)


def aluno_turmas(df):
    students = {}
    df = df.dropna(subset=['MEDIA_FINAL'])

    situations = dict(Situation.SITUATIONS)

    for matr, hist in df.groupby('MATR_ALUNO'):
        students[matr] = []

        for _, row in hist.iterrows():
            data = {
                'ano': str(int(row["ANO"])),
                'codigo': row["COD_ATIV_CURRIC"],
                'nome': row["NOME_ATIV_CURRIC"],
                'nota': row["MEDIA_FINAL"],
                'semestre': row["PERIODO"],
                'situacao': situations.get(row["SITUACAO"], Situation.SIT_OUTROS)
            }

            students[matr].append(data)

    return students
