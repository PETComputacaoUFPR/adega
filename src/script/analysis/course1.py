# -*- coding: utf-8 -*-
import copy
from datetime import datetime
import pprint
import pandas as pd
import json
import numpy as np
from script.utils.situations import Situation as sit
from collections import namedtuple
            memo[x] = f(b,x2,x3)
        return copy.deepcopy(memo[x])
    return helper

rate = namedtuple("rate",["name","column_name","fields_x","fields_X"])  
class Analysis(object):
    cache = {} 
    def __get_sum(self,serie,x=None):
        if x == None:
            return serie.sum() 

        temp = serie.iloc[serie.index.isin(x)].sum() 
        return temp

    def __rate(self,serie,x):
        serie_str = str(serie) 
        x_str = (str(x[0]) + serie_str, str(x[1]) + serie_str) 
        calc = [0,0] 

        if serie_str in self.cache:
            serie_count = self.cache[serie_str] 
        else:
            serie_count = serie.value_counts() 
            self.cache[serie_str] = serie_count 
        

        for i in range(len(calc)):
            if x_str[i] in self.cache:
                calc[i] = self.cache[x_str[i]] 
            else:
                calc[i]  = self.__get_sum(serie_count,x[i])
                self.cache[x_str[i]] = calc[i]  

        rate_value = np.divide(calc[0] ,np.float32(calc[1])) if calc[1] !=0 else -1 
        return (rate_value,calc[0] ,calc[1] ) 

    def _calc_rates(self,group,rates_set):
        group_dict = {} 

        for i in group:
            group_dict[i[0]] = [] 
            for j in rates_set: 
                serie = i[1][j.column_name]  
                temp = self.__rate(serie,(j.fields_x,j.fields_X))
                group_dict[i[0]].append((j.name,temp))  
        return group_dict

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
    course.calc_general_rate() 
    course.calc_semestral_rate() 
    #course.print() 
    #course.rate(course.general_df[1].SITUACAO,"teste") 
    #print(course.count) 


