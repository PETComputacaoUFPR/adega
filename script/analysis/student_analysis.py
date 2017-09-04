import pandas as pd
import numpy as np
import math
from utils.situations import Situation, EvasionForm


def ira_student(df):
   
    #total_graduate = df[df.FORMA_EVASAO == EvasionForm.EF_FORMATURA].shape[0]

    #~ return total_graduate / total_student
    Students = {}
    for i,line in enumerate(df.values):
        grr = df['MATR_ALUNO'][i]
        nota = df['MEDIA_FINAL'][i]
        carga_total = df['CH_TOTAL'][i]
        credito = df['MEDIA_CREDITO'][i]
        situacao = df['SITUACAO'][i]
        if(not grr in Students):
            Students[grr] = {
                "MEDIA_TOTAL": {"nota":0.0, "total":0, "carga_total": 0},
            }
        if(situacao in Situation.SITUATION_AFFECT_IRA and credito > 0):            
            Students[grr]["MEDIA_TOTAL"]["nota"]+=carga_total*nota
            Students[grr]["MEDIA_TOTAL"]["total"]+=1
            Students[grr]["MEDIA_TOTAL"]["carga_total"]+=carga_total
        if(situacao in Situation.SITUATION_PASS and credito > 0):            
            Students[grr]["APROVADAS"]=Students[grr].get("APROVADAS",0)+1
        if(situacao in Situation.SITUATION_FAIL and credito > 0):            
            Students[grr]["REPROVADAS"]=Students[grr].get("REPROVADAS",0)+1
    
    for s in Students:
        
        if((Students[s]["MEDIA_TOTAL"]["carga_total"]) > 0):
            Students[s]["MEDIA_TOTAL"]["nota"]/=(Students[s]["MEDIA_TOTAL"]["carga_total"])
        print(str(s)+" : "+str(Students[s]["MEDIA_TOTAL"]["nota"]))
        print(str(Students[s].get("APROVADAS"))+" "+str(Students[s].get("REPROVADAS")))
        print("")
    #~ print(Students)
    print(len(Students))
    return 1
