from pathlib import Path
import json
import csv


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

    # Feito o cabeçalho da planilha csv studentsimport csv


def create_csv(name_spreadsheet,name_columns,number_row):
    with open(name_spreadsheet, 'w') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(name_columns)
        
        content = []

        for i in name_columns:
            content.append(-1)

        for i in range(number_row):
            thewriter.writerow(content)

    #   name_spreadsheet = string com nome da planilha a ser criada
    #   name_columns = lista com nomes das colunas
    #   number_lines = qtd de linhas do csv
    
if __name__ == '__main__':
    #teste da funcao create_csv
    #lista = ['coluna1','coluna70','coluna22','coluna42']
    #create_csv('testeDaFuncao.csv', lista, 7)
