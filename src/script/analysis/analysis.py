# -*- coding: utf-8 -*-
import numpy as np
from script.utils.situations import Situation as sit
from collections import namedtuple
"""
Rate é uma tupla nomeada(deixa mais legivel fazer rate.name do que rate[0]) o
campo name define qual nome da taxa sera utilizado, collumn_name é qual coluna
do dataframe será utilizado para extrair dados, fields_x quais lista de valores
especifico será utilizado (numerador da taxa), fields_X é a lista de valores
gerais (denominador da taxa) e count_sel, assume valores 1 e 2, define qual quantidade será utilizada a
especifica ou a geral.
"""
rate = namedtuple("rate", ["name", "collumn_name", "fields_x", "fields_X", "count_sel"])
mean = namedtuple("mean", [
    "name",
    "collumn_name",
    "include_fields",
    "sum_collumn"
])


class Analysis(object):
    def sum_interval(self, df, col_filter, min_v, max_v, col_sum=None):
        """
        Soma os valores contindo no intervalo fechado min_v e max_v.
        """
        col_sum = col_filter if col_sum is None else col_sum

        df_filted = df.loc[
            (df[col_filter] >= float(min_v)) &
            (df[col_filter] <= float(max_v))
        ]
        serie = df_filted[col_sum].sum()
        return serie

    def count(self, group, collumn=None, _filter=None):
        """
        Conta a quantidade de linhas de cada dataframe de um groupby.

        Conta a quantidade linhas de cada dataframe, se collumn e _filter
        não forem None então cada dataframe é filtrado antes de contar as 
        linhas.
        """
        if collumn is None or _filter is None:
            return group.apply(lambda x: x.shape[0])
        serie = group.apply(lambda x: x[x[collumn].isin(_filter)].shape[0])
        return serie

    def calc_rate(self, groups, rates):
        """
        Calcula uma serie de taxa a partir de um groupby objects.

        Calcula todas as taxas contida na lista rates para todos os dataframes
        que estão dentro do groupby object groups.
        O calculo de uma taxa, para um dataframe em especifico é feito da
        seguinte maneira: filtra se o dataframe de acordo com os valores da
        especificado em rate.collumn_name com os valores de rate.field_x para o
        numerador e rate.fields_X para o denominador, a taxa é a divisão do
        numerador pelo denominador.
        Parametros:
            groups: groupby objects, contêm todos os dataframes, aplicado o
                o calculo da analise.
            rates: lista de namedtuples rate, utilizado para calcular taxas de
                forma generica
        Retorno:
            rate_dict: Dicionario python, no qual as chaves são o nome da taxa
            (rate.name) e o valores são pandas series.

        """
        rate_dict = {}

        for rate in rates:
            x = self.count(groups, rate.collumn_name, rate.fields_x)
            X = self.count(groups, rate.collumn_name, rate.fields_X)
            rate_c = x/X 
            rate_c[np.isnan(rate_c)] = 0.0
            rate_c[np.isinf(rate_c)] = 0.0
            rate_dict[rate.name] = [rate_c, x, X]
        return rate_dict


