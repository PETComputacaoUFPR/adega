import re
import pandas as pd
import numpy as np
from utils.situations import *

def average_ira(df):
    print(df)
    new_df = df.dropna(subset=['MEDIA_FINAL'])
    new_df = new_df[new_df['MEDIA_FINAL'] <= 100]
    if not new_df.empty:
        grade = np.sum(new_df['MEDIA_FINAL']*new_df['CH_TOTAL'])
        total_ch = np.sum(new_df['CH_TOTAL']) * 100

    return grade/total_ch

def pass_rate(dt):
    new_dt = dt[dt['SITUACAO'].isin(Situation.SITATUION_PASS)]
    
