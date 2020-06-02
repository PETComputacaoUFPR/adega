from pathlib import Path
from conversor_weka import create_csv
from conversor_weka import list_json
import json
import csv

def cria_cabecalho(caminho, arquivo):
    f = open(caminho + arquivo, "r")
    contents = f.read()
    lista_student = json.loads(contents)

    columns = list(lista_students.keys())

    nomes_colunas_geral = ""
    for nome in columns:
        nomes_colunas_geral += nome + ','

    # Feito o cabeçalho da planilha csv geral
