# -*- coding: utf-8 -*-
import copy
from datetime import datetime
import pprint
import pandas as pd
import json
import numpy as np
from script.utils.situations import Situation as sit
from collections import namedtuple
def memoize(f):
    memo = {}
    def helper(b,x2,x3):
        x = str(x2) + str(x3)   
        if x not in memo:            
            memo[x] = f(b,x2,x3)
        return copy.deepcopy(memo[x])
    return helper

rate = namedtuple("rate",["name","column_name","fields_x","fields_X"])  
class Analysis(object):
    def __get_sum(self,serie,x=None):
        if x == None:
            return serie.sum() 

        temp = serie.iloc[serie.index.isin(x)].sum() 
        return temp

    def __rate(self,serie,x,X=None):
        serie_count = serie.value_counts() 

        parcial = self.__get_sum(serie_count,x) 
        total = self.__get_sum(serie_count,X)
        rate_value = np.divide(parcial,np.float32(total)) if total !=0 else -1 
        return (rate_value,parcial,total) 

    def _calc_rates(self,group,rates_set):
        group_dict = {} 

        for i in group:
            group_dict[i[0]] = [] 
            for j in rates_set: 
                temp = self.__rate(i[1][j.column_name],j.fields_x,j.fields_X) 
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
    course.print() 
    #course.rate(course.general_df[1].SITUACAO,"teste") 
    print(course.count) 


