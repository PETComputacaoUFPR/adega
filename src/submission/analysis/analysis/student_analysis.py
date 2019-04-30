import numpy as np

# TODO:
# FAZER CACHE DE TUDO
# AO CHAMAR A FUNCAO VERIFICAR SE TEM ALGO NA CACHE

from submission.analysis.utils.situations import *
from submission.analysis.utils.utils import memoize
import pandas as pd
from collections import defaultdict




class StudentAnalysis:
    data_frame = None

    def __init__(self, df, current_year, current_semester):
        self.data_frame = df
        self.current_year = current_year
        self.current_semester = current_semester

    @memoize
    def student_info(self, df=None):
        df = df if df is not None else self.data_frame
        students = df.groupby([
            "MATR_ALUNO",
            "NOME_PESSOA",
            "ANO_INGRESSO",
            "SEMESTRE_INGRESSO",
            "ANO_EVASAO",
            "SEMESTRE_EVASAO",
            "FORMA_EVASAO",
        ])

        students = students.groups.keys()
        iras = self.ira_alunos(df=df)
        info = {}

        for stnd in students:
            grr = stnd[0]
            
            info[grr] = {
                "grr": grr,
                "name": str(stnd[1]),
                "ano_ingresso": str(stnd[2]),
                "semestre_ingresso": str(stnd[3]),
                "ano_evasao": str(stnd[4]),
                "semestre_evasao": str(stnd[5]),
                "forma_evasao": EvasionForm.code_to_str(stnd[6]),
                "ira": iras[grr],
            }
        return info

    @memoize
    def list_students(self, df=None):
        df = df if df is not None else self.data_frame
        situations = df.groupby(["MATR_ALUNO", "NOME_PESSOA", "FORMA_EVASAO"])
        situations = list(pd.DataFrame(
            {'count': situations.size()}).reset_index().groupby(["FORMA_EVASAO"]))

        iras = self.ira_alunos(df=df)
        list_situations = defaultdict(list)
        for sit in situations:
            grrs = list(sit[1]["MATR_ALUNO"])
            people_names = list(sit[1]["NOME_PESSOA"])

            evasion_form_name = EvasionForm.code_to_str(sit[0])

            for i, student in enumerate(grrs):
                list_situations[sit[0]].append({
                    "forma_evasao": evasion_form_name,
                    "grr": grrs[i],
                    "ira": iras[grrs[i]],
                    "nome": people_names[i]
                })

        return list_situations

    @memoize
    def ira_alunos(self, df=None):
        """
        Calculates the average IRA per student
        IRA = Sum (grades X coursetime)/ (total course time X 100)

        Parameters
        ----------
        df

        Returns
        -------
        dict

        Example
        --------
        iras = { GRR: number, ...}
        """
        df = df if df is not None else self.data_frame

        iras = self.ira_por_quantidade_disciplinas(df=df)
        ira_per_student = {}
        for i in iras:
            ira_total = 0
            carga_total = 0
            for semestre in iras[i]:

                ira_total += iras[i][semestre][0]*iras[i][semestre][2]
                carga_total += iras[i][semestre][2]

            if(carga_total != 0):
                ira_per_student[i] = ira_total/carga_total
            else:
                ira_per_student[i] = 0
        return ira_per_student

    @memoize
    def taxa_aprovacao(self, df=None):
        df = df if df is not None else self.data_frame

        aprovacoes_semestres = self.indice_aprovacao_semestral(df=df)

        for aluno in aprovacoes_semestres:
            total = sum([aprovacoes_semestres[aluno][s][1]
                         for s in aprovacoes_semestres[aluno]])
            aprovacoes = sum([aprovacoes_semestres[aluno][s][0]
                              for s in aprovacoes_semestres[aluno]])
            total = float(total)
            aprovacoes = float(aprovacoes)
            if(total != 0):
                aprovacoes_semestres[aluno] = aprovacoes/total
            else:
                aprovacoes_semestres[aluno] = None

        return aprovacoes_semestres

    def turma_ingresso(self, df=None):
        df = df if df is not None else self.data_frame
        df = df.drop_duplicates(subset="MATR_ALUNO", keep="first")
        admissions = {}
        for i, std in df.iterrows():
            admissions[std["MATR_ALUNO"]] = std["ANO_INGRESSO_y"] + \
                "/"+std["SEMESTRE_INGRESSO"]
        return admissions

    @memoize
    def posicao_turmaIngresso_semestral(self, df=None):
        df = df if df is not None else self.data_frame

        grr_to_admissions = self.turma_ingresso(df=df)

        admissions = defaultdict(list)

        # Create an dict of list where each key represent an admission class,
        # and its values represents the set of students
        # By instance: {"2015/1":["GRR20151346","GRR20154562", ...], ...}
        for grr in grr_to_admissions:
            admissions[grr_to_admissions[grr]].append(grr)


        iras_by_semester = self.ira_semestral(df=df)
        positions = defaultdict(dict)
        for grr in iras_by_semester:
            for semester in iras_by_semester[grr]:
                student_admission = admissions[grr_to_admissions[grr]]

                competition = [
                    matr for matr in student_admission if semester in iras_by_semester[matr]]

                classifications = sorted(
                    competition,
                    key=lambda matr: iras_by_semester[matr][semester]
                )
                positions[grr][semester] = (
                    1+classifications.index(grr))/len(competition)

        return positions

    @memoize
    def periodo_real(self, df=None):
        df = df if df is not None else self.data_frame

        aux = df.groupby(["MATR_ALUNO"])
        students = {}
        # TODO: Calculate the real value
        for x in aux:
            students[x[0]] = None
        return students

    @memoize
    def periodo_pretendido(self, df=None):
        df = df if df is not None else self.data_frame

        aux = df.groupby(["MATR_ALUNO", "ANO_INGRESSO", "SEMESTRE_INGRESSO"])
        students = {}
        for x in aux:
            students[x[0][0]] = ((self.current_year - int(x[0][1])) * 2 +
                                 self.current_semester - int(x[0][2]) + 1)
        return students

    @memoize
    def ira_semestral(self, df=None):
        df = df if df is not None else self.data_frame

        aux = self.ira_por_quantidade_disciplinas(df=df)
        for matr in aux:
            for periodo in aux[matr]:
                aux[matr][periodo] = aux[matr][periodo][0]
        return aux

    @memoize
    def ira_por_quantidade_disciplinas(self, df=None):
        """
        Calculates the ira per year/semester

        Parameters
        ----------
        df : seila

        Returns
        -------
        dict of dict of array
        iras = { GRR: {year/semester: []},
        ...}

        Example
        --------

        """
        df = df if df is not None else self.data_frame

        students = {}
        df = df.dropna(subset=["MEDIA_FINAL"])

        total_students = len(df["MATR_ALUNO"])
        for i in range(total_students):
            matr = df["MATR_ALUNO"][i]
            if (not (matr in students)):
                students[matr] = {}

            ano = str(int(df["ANO"][i]))
            semestre = str(df["PERIODO"][i])
            situacao = int(df["SITUACAO"][i])
            nota = float(df["MEDIA_FINAL"][i])
            carga = float(df["CH_TOTAL"][i])

            if (situacao in Situation.SITUATION_AFFECT_IRA):
                if not (ano + "/" + semestre in students[matr]):
                    students[matr][ano + "/" + semestre] = [0, 0, 0]

                students[matr][ano + "/" + semestre][0] += nota*carga
                students[matr][ano + "/" + semestre][1] += 1
                students[matr][ano + "/" + semestre][2] += carga

        for matr in students:
            for periodo in students[matr]:
                if (students[matr][periodo][2] != 0):
                    students[matr][periodo][0] /= students[matr][periodo][2] * 100

        return students

    @memoize
    def indice_aprovacao_semestral(self, df=None):
        df = df if df is not None else self.data_frame

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

    @memoize
    def aluno_turmas(self, df=None):
        """

        Returns
        -------
        dict of

        Example
        --------
        """
        df = df if df is not None else self.data_frame

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
