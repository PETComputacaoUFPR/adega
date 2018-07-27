# -*- coding: utf-8 -*-
import pprint
import pandas as pd
import json
import numpy as np
from script.utils.situations import Situation as sit
from collections import namedtuple

rate = namedtuple("rate",["name","column_name","fields_x","fields_X"])
mean = namedtuple("mean",["name","collumn_name","include_fields","sum_collumn"]) 

class Analysis(object):
    """
    Realiza operações analiticas sobre dataframes e series.

    Classe base que possui alguns metodos de calculo estastico
    elaborado sobre calculo de taxas e calculo de media.

    """
    def _get_sum(self,serie,x=None):
        """
        Faz a soma de alguns elementosself.

        O metodo soma os valores da serie no qual a chave está contida
        em x. Se x for igual a None todos os valores da serie são 
        somados.

        """
        if x is None:
            return serie.sum()

        temp = serie.iloc[serie.index.isin(x)].sum()
        return temp

    def __rate(self,serie,x,X=None):
        """
        Calcula a taxa de x  sobre X serie
        """ 
        serie_count = serie.value_counts()
        calc = [self._get_sum(serie_count,x),self._get_sum(serie_count,X)]

        rate_value = np.divide(calc[0] ,np.float32(calc[1])) if calc[1] !=0 else -1
        return [rate_value,calc[0] ,calc[1]]

    def rates_calc(self,group,rates_set):
        group_dict = {}

        for i in group:
            group_index = i[0] 
            group_df = i[1] 
            group_dict[group_index] = {} 
            for j in rates_set:
                temp = self.__rate(group_df[j.column_name],j.fields_x,j.fields_X)
                group_dict[group_index][j.name] = temp
        return group_dict


    def _mean(self,df,collumn_sum,collumn_name,serie_collumn=None): 
        if serie_collumn is not None:
            df_filted = df[df[collumn_name].isin(serie_collumn)] 
        else:
            df_filted = df

        mean = df_filted[collumn_sum].mean()  
        std = df_filted[collumn_sum].std()  
        count = df_filted[collumn_sum].shape[0]  
        return [mean,std,count] 

    def mean_calc(self,group_df,mean_set):
        group_mean_dict = {}
        for i in group_df:
            grouped_df = i[1] 
            grouped_index = i[0] 
            group_mean_dict[grouped_index] = {} 
            for j in mean_set:
                mean_set_result = self._mean(grouped_df,j.sum_collumn,j.collumn_name,j.include_fields) 
                group_mean_dict[grouped_index][j.name] = mean_set_result  
        return group_mean_dict

class Course(Analysis):
    __general_groupby_df = None
    __semestral_groupby_df = None
    __df = None
    __build_analyze = False
    courses = None
    general_rate = None
    semestral_rate = None
    general_mean = None
    semestral_mean = None
    semestral_count_application = None
    general_count_application = None
    __rates = [
                rate("taxa_reprovacao_absoluta",
                    "SITUACAO",
                    list(sit.SITUATION_FAIL),
                    list(sit.SITUATION_COURSED)),
                rate("taxa_aprovacao",
                    "SITUACAO",
                    list(sit.SITUATION_PASS),
                    list(sit.SITUATION_COURSED)),
                rate("taxa_trancamento",
                    "SITUACAO",
                    [sit.SIT_CANCELADO],
                    list(sit.SITUATION_COURSED)),
                rate("taxa_conhecimento",
                    "SITUACAO",
                    [sit.SIT_CONHECIMENTO_APROVADO],
                    list(sit.SITUATION_KNOWLDGE)),
                rate("taxa_reprovacao_frequencia",
                    "SITUACAO",
                    [sit.SIT_REPROVADO_FREQ],
                    list(sit.SITUATION_COURSED))
            ]
    __mean_set = [
            mean("nota",
                 "SITUACAO",
                 list(sit.SITUATION_AFFECT_IRA),
                 "MEDIA_FINAL")
            ] 
    def __init__(self,df):
        self.df = df
        self.__general_groupby_df = df.groupby(["COD_ATIV_CURRIC"])
        self.__semestral_groupby_df = df.groupby(["COD_ATIV_CURRIC","ANO","PERIODO"])
    def build_analysis(self):
        self.courses_list() 
        self.calc_general_count_submission() 
        self.calc_semestral_count_submission() 
        self.calc_general_rate()
        self.calc_general_mean()
        self.calc_semestral_rate() 
        self.calc_semestral_mean() 

        self.__build_analyze = True

    def generate_cache_dict(self):
        pp = pprint.PrettyPrinter(indent=4)
        cache = {} 
        compara_aprov = {} 
        if self.__build_analyze is False:
            self.build_analysis() 

        for course in self.courses:
            cache[course] = {**self.general_mean[course],**self.general_rate[course]}  
            compara_aprov[course] = [] 

        for i in self.semestral_rate:
            period = str(i[1])+'/'+str(i[2])   
            compara_aprov[i[0]].append([period,self.semestral_rate[i]['taxa_aprovacao']])


    def print(self):
        pp = pprint.PrettyPrinter(indent=4)
        print_list = [
               (self.general_mean,"General mean course\n"), 
               (self.general_rate,"General rate course\n"),
               (self.general_count_application,"general application count\n"),
               (self.semestral_mean,"Semestral mean course\n"),
               (self.semestral_rate,"semestral rate course\n"),
               (self.semestral_count_application,"semestral application count\n")
                ] 
        for i in print_list:
            if i[0] is not None:
                print(i[1]) 
                pp.pprint(i[0])

    def calc_general_rate(self):
        self.general_rate = self.rates_calc(self.__general_groupby_df,self.__rates)

    def calc_semestral_rate(self):
        self.semestral_rate = self.rates_calc(self.__semestral_groupby_df,self.__rates)

    def calc_general_mean(self):
        self.general_mean = self.mean_calc(self.__general_groupby_df,self.__mean_set) 

    def calc_semestral_mean(self):
        self.semestral_mean = self.mean_calc(self.__semestral_groupby_df,self.__mean_set) 

    def calc_general_count_submission(self): 
        submission_count_serie =  self.__general_groupby_df.apply(lambda x: x.shape[0])
        self.general_count_application = submission_count_serie.to_dict() 

    def courses_list(self):
        self.courses = self.df['COD_ATIV_CURRIC'].drop_duplicates()
        self.courses = self.courses.tolist() 

    def calc_semestral_count_submission(self): 
        submission_count =  self.__general_groupby_df.apply(lambda x: x.shape[0])
        self.semestral_count_application = submission_count.to_dict() 

    def save_json(self):
        pass

def make_course(df):

    a = Course(df)
    #a.calc_general_count_submission() 
    #a.calc_semestral_count_submission() 
    #a.calc_general_rate()
    a.calc_general_mean()
    #a.calc_semestral_rate() 
    #a.calc_semestral_mean() 
    #a.print() 

