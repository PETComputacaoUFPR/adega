import pandas as pd
import math
import ujson as json
from utils.situations import Situation, EvasionForm

def alunos_por_periodo(df):
    alunos_periodo = {}
    limite = int(df['PERIODO_IDEAL'].max()) + 1
    alunos_p = df.loc[(df.PERIODO != 'Anual') & (df.PERIODO != 'Semestral') & (df.PERIODO != 'Perí')]
    ano = int(alunos_p['ANO'].max()) - 1
    periodo = int(alunos_p['PERIODO'].max())
    alunos_p = alunos_p.loc[alunos_p['ANO'] == (ano)]
    alunos_p = alunos_p.loc[alunos_p['PERIODO'] == str(periodo)]
    alunos_p = alunos_p.sort_values(by=['PERIODO_IDEAL'])
    alunos_p = alunos_p.dropna(subset=['PERIODO_IDEAL'])
    alunos_p = alunos_p.drop_duplicates('MATR_ALUNO', keep='last')
    alunos_p = alunos_p.loc[(alunos_p.FORMA_EVASAO == EvasionForm.EF_ATIVO)]
    for i in range(1,limite):
        alunos_periodo[i] = (alunos_p.loc[(alunos_p['PERIODO_IDEAL'] == i) | (alunos_p['PERIODO_IDEAL'] == i%(limite-1))]).shape[0]
    return alunos_periodo

def taxa_aprovacao_periodo(df):
    aprovacao_periodo = {}
    limite = int(df['PERIODO_IDEAL'].max()) + 1
    alunos_p = df[df.SITUACAO.isin(Situation.SITUATION_AFFECT_IRA)]
    aprovacao_p = alunos_p[alunos_p.SITUACAO.isin(Situation.SITUATION_PASS)]
    for i in range(1,limite):
        al_p = alunos_p.loc[(alunos_p['PERIODO_IDEAL'] == i)].shape[0]
        ap_p = aprovacao_p.loc[aprovacao_p['PERIODO_IDEAL'] == i].shape[0]
        aprovacao_periodo[i] = ap_p / al_p
    return aprovacao_periodo

def nota_media_periodo(df):
    ira_periodo = {}
    limite = int(df['PERIODO_IDEAL'].max()) + 1
    ira_p = df[df.SITUACAO.isin(Situation.SITUATION_AFFECT_IRA)]
    ira_p = ira_p[ira_p.MEDIA_FINAL <= 100]
    for i in range(1,limite):
        i_p = ira_p.loc[ira_p['PERIODO_IDEAL'] == i]
        ira_periodo[i] = i_p.MEDIA_FINAL.mean()
    return ira_periodo
    
def novas_analises_json(df):
    cache_novas_analises = {
		'alunos_por_periodo': json.dumps(alunos_por_periodo(df)),
		'taxa_aprovacao_periodo': json.dumps(taxa_aprovacao_periodo(df)),
		'nota_media_periodo': json.dumps(nota_media_periodo(df))
	}
    with open("cache/curso/novas_analises.json", 'w') as f:
        f.write(json.dumps(cache_novas_analises,indent=4))

