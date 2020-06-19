import json
import csv

import os
import argparse

import pandas as pd


from conversor_admissions import AdmissionConversor
from conversor_courses import CourseConversor
from conversor_students import StudentConversor

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help="name of the sheet",
                        required=True)
    # parser.add_argument('--output', type=str,help="path to sheet",
    #                     required=True)
    # parser.add_argument('--type_input', type=str,help="input type",
    #                     required=False, default="SIE")
    # parser.add_argument('--output_fname', type=str,help="output file name",
    #                     required=False, default="adega_input.csv")
    args = parser.parse_args()

    return args




def main():
    args = get_args()
    submission_path = args.input

    '''
    admission = AdmissionConversor(submission_path)
    data_admission,header_admission = admission.get_admission_as_matrix()
    df = pd.DataFrame(data_admission)
    df.columns = header_admission
    # print(df[["Ano","Período","students_per_semester_StudentsCount_2015_1o. Semestre"]])
    # print(df[["Ano","Período","ira_per_semester_std_2013_1o. Semestre"]])
    print(df)
    '''

    '''
    course = CourseConversor(submission_path)
    data_course,header_course = course.get_course_as_matrix()
    df = pd.DataFrame(data_course)
    df.columns = header_course
    print(df[["Código","Nome","aprovacao_semestral_QuantidadeAprovacao_2015_1o. Semestre"]])
    print(df[["Código","Nome","grafico_qtd_cursada_aprov_QuantidadeDeVezesCursadaAteAprovacao_1"]])
    print(df[["Código","Nome","grafico_qtd_cursada_aprov_QuantidadeDeVezesCursadaAteAprovacao_2"]])
    print(df[["Código","Nome","grafico_qtd_cursada_aprov_QuantidadeDeVezesCursadaAteAprovacao_MaisQue4"]])
    '''

    student = StudentConversor(submission_path)
    data_student,header_student = student.get_student_as_matrix()
    df = pd.DataFrame(data_student)
    df.columns = header_student
    # print(df[["Código","Nome","aprovacao_semestral_QuantidadeAprovacao_2015_1o. Semestre"]])
    # print(df[["Código","Nome","grafico_qtd_cursada_aprov_QuantidadeDeVezesCursadaAteAprovacao_1"]])
    # print(df[["Código","Nome","grafico_qtd_cursada_aprov_QuantidadeDeVezesCursadaAteAprovacao_2"]])
    # print(df[["Código","Nome","grafico_qtd_cursada_aprov_QuantidadeDeVezesCursadaAteAprovacao_MaisQue4"]])
    print(df)

if __name__ == '__main__':
    main()
    #teste da funcao create_csv
    #lista = ['coluna1','coluna70','coluna22','coluna42']
    #create_csv('testeDaFuncao.csv', lista, 7)
