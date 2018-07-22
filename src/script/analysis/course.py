# -*- coding: utf-8 -*-
import pprint
import pandas as pd
import json
import numpy as np
from script.utils.situations import Situation as sit
from collections import namedtuple

rate = namedtuple("rate",["name","column_name","fields_x","fields_X"])  

class Analysis(object):
    def __get_sum(self,serie,x=None):
        if x == None:
            return serie.sum() 

        temp = serie.iloc[serie.index.isin(x)].sum() 
        return temp

    def __rate(self,serie,x,X=None):
        serie_count = serie.value_counts() 
        calc = [self.__get_sum(serie_count,x),self.__get_sum(serie_count,X)] 

        rate_value = np.divide(calc[0] ,np.float32(calc[1])) if calc[1] !=0 else -1 
        return (rate_value,calc[0] ,calc[1] ) 

    def _calc_rates(self,group,rates_set):
        group_dict = {} 

        for i in group:
            group_dict[i[0]] = [] 
            for j in rates_set: 
                temp = self.__rate(i[1][j.column_name],j.fields_x,j.fields_X)
                group_dict[i[0]].append((j.name,temp))  
        return group_dict

    def __mean(self,df,mean_set):
        df_filtre = df.loc[df..values.isin(mean_set)] 

    def _calc_mean(self,group,mean_set):
        group_mean_dict = {} 
        for i in group:
            group_mean_dict[i[0]] = [] 
            temp = self.__mean(i[1],mean_set) 
            break

class Course(Analysis):
    __general_groupby_df = None
    __semestral_groupby_df = None
    __general_rate = None
    __semestral_rate = None
    __rates = [
                rate("absolute_reprovation",
                    "SITUACAO",
                    list(sit.SITUATION_FAIL),
                    list(sit.SITUATION_COURSED)), 
                rate("aprovation",
                    "SITUACAO",
                    list(sit.SITUATION_PASS),
                    list(sit.SITUATION_COURSED)),
                rate("trancamento",
                    "SITUACAO",
                    [sit.SIT_CANCELADO],
                    list(sit.SITUATION_COURSED)),
                rate("conhecimento",
                    "SITUACAO",
                    [sit.SIT_CONHECIMENTO_APROVADO],
                    list(sit.SITUATION_CONHECIMENTO)),
                rate("frequency_reprovation",
                    "SITUACAO",
                    [sit.SIT_REPROVADO_FREQ],
                    list(sit.SITUATION_COURSED)) 
            ] 
    def __init__(self,df):
        self.__general_groupby_df = df.groupby(["COD_ATIV_CURRIC"]) 
        self.__semestral_groupby_df = df.groupby(["COD_ATIV_CURRIC","ANO","PERIODO"]) 

    def print(self):
        pp = pprint.PrettyPrinter(indent=4)
        if self.__general_rate is not None:
            print("General rates course\n") 
            pp.pprint(self.__general_rate) 
        if self.__semestral_rate is not None:
            print("Semestral rates course\n") 
            pp.pprint(self.__semestral_rate) 

    def calc_general_rate(self):
        self.__general_rate = self._calc_rates(self.__general_groupby_df,self.__rates) 

    def calc_semestral_rate(self): 
        self.__semestral_rate = self._calc_rates(self.__semestral_groupby_df,self.__rates) 

def make_course(df): 

    course = Course(df)
    #course.calc_general_rate() 
    #course.calc_semestral_rate() 


