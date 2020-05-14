from pathlib import Path
import json

def list_json(caminho, lista):

    path = Path(caminho) ### . == path

    for filename in path.glob('*'):
        if (filename.suffix == ".json"):
            lista.append(str(filename))
        else: 
            temp = caminho + "/" + str(filename)
            list_json(temp, lista)

def cria_cabecalho(caminho):
    f = open(caminho + "/lista_turma_ingresso.json", "r")
    contents = f.read()
    lista_turma_ingresso = json.loads(contents)

    nomes_colunas_geral = ""
    for nome in lista_turma_ingresso[0]:
        if (nome != "ira_per_semester" and
            nome != "students_per_semester" and
            nome != "evasion_per_semester"):
            nomes_colunas_geral += nome + ','

    nomes_colunas_geral += "formatura_media,taxa_reprovacao,taxa_evasao"

    # Feito o cabeçalho da planilha csv geral

    nomes_colunas_ira = []

    for linha in range(len(lista_turma_ingresso)):
        for nome in lista_turma_ingresso[linha]["ira_per_semester"]:
            if (not (nome in nomes_colunas_ira)):
                nomes_colunas_ira.append(nome)

    # Feito o cabeçalho da planilha csv ira

    nomes_colunas_students = []

    for linha in range(len(lista_turma_ingresso)):
        for nome in lista_turma_ingresso[linha]["students_per_semester"]:
            if (not (nome in nomes_colunas_students)):
                nomes_colunas_students.append(nome)

    # Feito o cabeçalho da planilha csv students