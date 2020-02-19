# -*- coding: utf-8 -*-
from submission.analysis.conversor_de_dados_adega.utils.situations import Situation as sit
from submission.analysis.analysis.analysis import Analysis, rate, mean
import numpy as np


class Course(Analysis):
    """
    Classe que calcula analises relacionada a disciplina.

    """
    __data = {}
    __build_analyze = False
    analysis = dict.fromkeys([
        "courses",
        "general_rate",
        "semestral_rate",
        "general_mean",
        "semestral_mean",
        "semestral_count_application",
        "general_count_application",
        "coursed_count",
        "graph_course"
    ], None)

    __rates = [
        rate(
            "taxa_reprovacao_absoluta",
            "SITUACAO_ATIV_CURRIC",
            list(sit.SITUATION_FAIL),
            list(sit.SITUATION_COURSED),
            1
        ),
        rate(
            "taxa_aprovacao",
            "SITUACAO_ATIV_CURRIC",
            list(sit.SITUATION_PASS),
            list(sit.SITUATION_FAIL) + list(sit.SITUATION_PASS),
            2
        ),
        rate(
            "taxa_trancamento",
            "SITUACAO_ATIV_CURRIC",
            list(sit.SITUATION_CANCELLED),
            list(sit.SITUATION_COURSED),
            1
        ),
        rate(
            "taxa_conhecimento",
            "SITUACAO_ATIV_CURRIC",
            [sit.SIT_CONHECIMENTO_APROVADO],
            list(sit.SITUATION_KNOWLDGE),
            2
        ),
        rate(
            "taxa_reprovacao_frequencia",
            "SITUACAO_ATIV_CURRIC",
            [sit.SIT_REPROVADO_FREQ],
            list(sit.SITUATION_COURSED),
            1
        )
    ]
    __mean_set = [
        mean("nota",
             "SITUACAO_ATIV_CURRIC",
             list(sit.SITUATION_AFFECT_IRA),
             "MEDIA_FINAL")
    ]
    __semestral_rate = [__rates[1]]
    last_rate = [__rates[0], __rates[4]]

    def __init__(self, current_year, df):
        self.current_year = current_year
        df_filted = df[df['SITUACAO_ATIV_CURRIC'].isin(sit.SITUATION_COURSED)]
        dict_df = {
            "normal_dataframe": df,
            "filted_dataframe": df_filted
        }
        for df in dict_df:
            type_df = df.split("_")[0] + "_"
            general_tmp = dict_df[df].groupby(["COD_ATIV_CURRIC"])
            semestral_tmp = dict_df[df].groupby(
                ["COD_ATIV_CURRIC", "ANO_ATIV_CURRIC", "PERIODO_ATIV_CURRIC"])
            self.__data[type_df + "general_groupby"] = general_tmp
            self.__data[type_df + "semestral_groupby"] = semestral_tmp
            self.__data[df] = dict_df[df]

    def __str__(self):
        """
        Retorna uma string com todas as analises feita no momento.
        """
        analysis = []
        for analyze in self.analysis:
            if self.analysis[analyze] is not None:
                analysis.append(self.analysis[analyze])
        return "Analises: {} \n".format(analysis)

    def build_analysis(self):
        """
        Chama todos os metodos de analises.
        O metodo é responsável por fazer todas analises necessarias
        para disciplina, ao final de fazer todas as analises o metodo muda o
        valor do atributo self.__build_analyze para True, desta maneira não é
        necessario executar uma analises, se ela já foi feita.

        """
        self.courses_list()
        self.general_rate()
        self.semestral_rate()
        self.general_count_submission()
        self.semestral_count_submission()
        self.graph_course()
        self.coursed_count()
        self.general_note_statistic()
        self.last_year_rate()

        self.__build_analyze = True

    def courses_list(self):
        """
        Obtém a lista de disciplina de um curso.

        A lista de disciplina de um curso se resume em uma serie (pandas),
        no qual o valor é o nome da disciplina e o index é o código da
        disciplina.
        A serie é obtida por meio do dataframe df, em que é retirado todas as
        linhas em que o valor da coluna COD_ATIV_CURRIC é duplicado, e redinido
        o index para a coluna COD_ATIV_CURRIC, assim é possivel obter a serie.

        """
        df = self.__data["filted_dataframe"]
        df = df[["COD_ATIV_CURRIC", "NOME_ATIV_CURRIC"]].drop_duplicates()
        df = df.set_index("COD_ATIV_CURRIC")
        self.analysis["courses"] = df["NOME_ATIV_CURRIC"]

    def last_year_rate(self):
        # reprovaçao rate

        last_rates = self.last_rate

        def f(x, rate):
            x1 = x.loc[x.ANO_ATIV_CURRIC == x.ANO_ATIV_CURRIC.max() - 1]
            x_num = x1[x1[rate.collumn_name].isin(rate.fields_x)].shape[0]
            x_deno = x1[x1[rate.collumn_name].isin(rate.fields_X)].shape[0]
            return x_num / x_deno if x_deno > 0 else 0

        groups = self.__data["normal_general_groupby"]
        for r_it in last_rates:
            g = groups.apply(lambda x: f(x, r_it))
            self.analysis["last_year_" + r_it.name] = g

    def general_rate(self):
        """
        Calcula as taxas gerais para cada disciplina e a media das taxas.

        O calculo das taxas para cada disciplina utiliza o metodo da super
        classe Analysis calc_rate, no qual é passado um groupby object e Uma
        lista de taxas a serem calculadas. O calculo da media das taxas é feito
        calculando a media das taxas de cada dataframes do
        groupby object groups.
        """
        groups = self.__data["normal_general_groupby"]
        rates = self.calc_rate(groups, self.__rates)
        self.analysis["general_rates"] = rates
        # calculo das rates do ultimo ano
        # calcula estastistica gerais de todas disciplina
        for rate_it in self.__rates:
            rate_mean = self.analysis["general_rates"][rate_it.name][0].mean()
            rate_std = self.analysis["general_rates"][rate_it.name][0].std()
            self.analysis[rate_it.name] = [rate_mean, rate_std]

    def semestral_rate(self):
        """
        Calcula as taxas de modo semestrais para cada disciplina.

        O calculo das taxas semestrais utiliza o metodo da super classe
        Analysis calc_rate, no qual é passado um groupby object e uma lista
        de taxas a serem calculadas.
        """
        groups = self.__data["normal_semestral_groupby"]
        rates = self.calc_rate(groups, [self.__rates[1]])
        self.analysis["semestral_rate"] = rates

    def semestral_count_submission(self):
        """
        calcula a quantidade de matriculas por semestre.

        calcula quantos alunos se matricularam na disciplina em cada
        semestre.

        """
        serie_count = self.count(self.__data["normal_semestral_groupby"])
        self.analysis["semestral_count_application"] = serie_count.to_dict()

    def general_note_statistic(self):
        """
        Calcula algumas estatisticas sobre MEDIA_FINAL relacionada a course.
        """
        group = self.__data["filted_general_groupby"]
        serie_mean = group.apply(lambda x: x["MEDIA_FINAL"].mean())
        serie_std = group.apply(lambda x: x["MEDIA_FINAL"].std())
        last_year_mean = group.apply(
            lambda x: x.loc[x.ANO_ATIV_CURRIC == x.ANO_ATIV_CURRIC.max() -
            1].MEDIA_FINAL.mean())
        last_year_std = group.apply(
            lambda x: x.loc[x.ANO_ATIV_CURRIC == x.ANO_ATIV_CURRIC.max() -
            1].MEDIA_FINAL.std())
        # caso tenha algum nan, troque por 0.0
        serie_mean[np.isnan(serie_mean)] = 0.0
        serie_std[np.isnan(serie_std)] = 0.0
        last_year_mean[np.isnan(last_year_mean)] = 0.0
        last_year_std[np.isnan(last_year_std)] = 0.0
        general_mean = serie_mean.mean()
        general_std = serie_std.mean()
        self.analysis["general_note_statistic"] = [serie_mean, serie_std]
        self.analysis["general_note_mean"] = general_mean
        self.analysis["general_note_std"] = general_std
        self.analysis["last_year_statistic"] = [last_year_mean, last_year_std]
        self.analysis["general_last_year_mean"] = last_year_mean.mean()
        self.analysis["general_last_year_std"] = last_year_std.mean()

    def general_count_submission(self):
        """
        Conta a quantidade de matriculas que cada disciplina tem.
        """
        serie_count = self.count(self.__data["normal_general_groupby"])
        self.analysis["general_count_submission"] = serie_count.to_dict()

    def __calc_graph_mean(self, group, min_v, max_v, graph):
        """
        Calcula a media que está entre um intervalo.
        Calcula a media das notas que estão ente o intervalo min_v e max_v e
        groupby.
        """
        interval_key = str(min_v) + "-" + str(max_v)
        col = "MEDIA_FINAL"

        # para ficar mais legivel
        def f(x, min_v, max_v):
            return self.sum_interval(x, col, min_v, max_v)

        graph_serie = group.apply(lambda x: f(x, min_v, max_v) / x.shape[0])
        graph_dict = graph_serie.to_dict()  # transforma em dicionario

        for course in graph_dict:  # coloca a media e o intervalo no dicionario
            graph[course].append([interval_key, graph_dict[course]])

    def graph_course(self):
        """
        Calcula o grafico de nota disciplina.
        """
        group = self.__data["filted_general_groupby"]
        graph = {}
        if self.analysis["courses"] is None:
            self.courses_list()

        # inicializa o dicionario que vai guardar o grafico
        for course in self.analysis["courses"].index:
            graph[course] = []

        for i in range(18):
            min_v = i * 5
            max_v = min_v + 4.99
            self.__calc_graph_mean(group, min_v, max_v, graph)

        min_v = 95
        max_v = 100
        self.__calc_graph_mean(group, min_v, max_v, graph)

        self.analysis["graph_course"] = graph

    def coursed_count(self):
        """
        Calcula a quantidade de vezes que cada aluno cursou a disciplina.
        """
        dict_name = "filted_course_student_groupby"
        self.__data[dict_name] = self.__data["normal_dataframe"].groupby([
            "COD_ATIV_CURRIC",
            "MATR_ALUNO"
        ])
        course_dict = {}
        for df in self.__data[dict_name]:
            if df[0][0] not in course_dict:
                course_dict[df[0][0]] = dict.fromkeys(
                    [str(i) for i in range(1, 6)], 0)
            count = df[1].shape[0] if df[1].shape[0] <= 5 else 5
            course_dict[df[0][0]][str(count)] += 1

        self.analysis["coursed_count"] = course_dict
        # ratio coursed count

        def f(x):
            coursed_succes = x[x['SITUACAO_ATIV_CURRIC'].isin(sit.SITUATION_PASS)].shape[0]
            return (x.shape[0] / coursed_succes) if coursed_succes > 0 else -1

        groups = self.__data["filted_dataframe"].groupby(["COD_ATIV_CURRIC"])
        ratio_coursed = groups.apply(lambda x: f(x))
        self.analysis["coursed_ratio"] = ratio_coursed.to_dict()

    def build_general_course(self):
        """
        Cria o dicionario para o json chamado 'disciplina.json'
        """

        courses = {}

        if self.__build_analyze is False:
            self.build_analysis()

        courses["taxa_conhecimento"] = self.analysis["taxa_conhecimento"]
        courses["taxa_reprovacao"] = self.analysis["taxa_reprovacao_absoluta"]
        courses["taxa_trancamento"] = self.analysis["taxa_trancamento"]

        # cria cache
        cache = {}
        note = self.analysis["general_note_statistic"]
        for rate_it in self.__rates:
            rate_calc = self.analysis["general_rates"][rate_it.name][0]
            for course in self.analysis["courses"].index:
                if course not in cache:
                    cache[course] = {}
                cache[course][rate_it.name] = rate_calc[course]
                cache[course]["nota"] = [note[0][course], note[1][course]]

        courses["cache"] = cache

        # cria o campo compara_aprov
        courses["compara_aprov"] = self.analysis["graph_course"]

        # cria o campo courses
        courses["disciplinas"] = self.analysis["courses"].to_dict()

        return courses

    def build_course(self):
        """
        Cria o dicionario para cada json de disciplina, ex 'CI055.json'.
        """
        courses = []
        aprovacao_d = {}
        # semestral
        for rate_it in self.__semestral_rate:
            # pega uma lista no qual o primeiro elemento é a taxa, o segundo
            # e o terceiro são quantidades
            rate_data = self.analysis["semestral_rate"][rate_it.name]
            for i in rate_data[0].index:
                if i[0] not in aprovacao_d:
                    aprovacao_d[i[0]] = {}

                periodo = str(i[1]) + "/" + str(i[2])
                aprovacao_d[i[0]][periodo] = [
                    float(rate_data[0][i]),
                    int(rate_data[1][i]),
                    int(rate_data[2][i]),]

        note = self.analysis["general_note_statistic"]
        note_last_year = self.analysis["last_year_statistic"]
        for course in self.analysis["courses"].index:
            course_dict = {}
            course_dict["disciplina_codigo"] = course
            course_dict["disciplina_nome"] = self.analysis["courses"][course]
            # quantidade de matriculas
            count = self.analysis["general_count_submission"][course]
            course_dict["qtd_alunos"] = count
            # notas
            course_dict["qtd_cursada_aprov"] = self.analysis["coursed_ratio"][course]
            course_dict["nota"] = [note[0][course], note[1][course]]
            course_dict["nota_ultimo_ano"] = [
                note_last_year[0][course],
                note_last_year[1][course]
            ]
            # taxas
            for rate_it in self.__rates:
                rate_data = self.analysis["general_rates"][rate_it.name]
                course_dict[rate_it.name] = float(rate_data[0][course])
                course_str = rate_it.name.replace("taxa", "qtd")
                # count_sel define qual quantidade vai para o json, a especifica
                # ou geral
                course_dict[course_str] = int(
                    rate_data[rate_it.count_sel][course])
                # rate_calc = self.analysis["general_rates"][rate_it.name][0]

            # taxas do ultimo anos
            course_dict["taxa_reprovacao_ultimo_absoluto"] = self.analysis["last_year_taxa_reprovacao_absoluta"][course]
            course_dict["taxa_reprovacao_ultimo_frequencia"] = self.analysis["last_year_taxa_reprovacao_frequencia"][course]

            course_dict["grafico_qtd_cursada_aprov"] = self.analysis["coursed_count"][course]
            course_dict["aprovacao_semestral"] = aprovacao_d[course]
            courses.append(course_dict)
        return courses
