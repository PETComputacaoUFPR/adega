import re
import os
import sys
import pandas as pd

from glob import glob
from json import load as json_load
from utils.situations import *


def load_dataframes(cwd='.'):
    dataframes = []
    for path, dirs, files in os.walk(cwd):       
        for f in files:
            file_path = path + '/' + f
            dh = {'name': f, 'dataframe': None}
            if 'csv' in f:
                dh['dataframe'] = read_csv(file_path)
            if 'xls' in f:
                dh['dataframe'] = read_excel(file_path)

            if dh['dataframe'] is not None:
                dataframes.append(dh)

    return dataframes

def read_excel(path, planilha='Planilha1'):
    return pd.read_excel(path)

def read_csv(path):
    return pd.read_csv(path)

def fix_dataframes(dataframes):
    for df in dataframes:
        fix_situation(df['dataframe'])

def fix_situation(df):
    if hasattr(df, 'SITUACAO'):
        for situation in Situation.SITUATIONS:
            df.loc[df.SITUACAO == situation[1], 'SITUACAO'] = situation[0]
            if situation[1] == 'Outro':
                temp = df[~df['SITUACAO'].astype(str).str.isdigit()]
                df.loc[~df.SITUACAO.astype(str).str.isdigit()] = situation[0]
