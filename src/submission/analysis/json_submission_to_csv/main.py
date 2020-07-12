import json
import csv
import os
import argparse
import pandas as pd
from zipfile import ZipFile

from submission.analysis.json_submission_to_csv.conversor_admissions import AdmissionConversor
from submission.analysis.json_submission_to_csv.conversor_courses import CourseConversor
from submission.analysis.json_submission_to_csv.conversor_students import StudentConversor

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help="name of the sheet",
                        required=True)
    parser.add_argument('--zip_path', type=str,
                        help="name of zip created with csv data",
                        required=false, default="test")
    # parser.add_argument('--output', type=str,help="path to sheet",
    #                     required=True)
    # parser.add_argument('--type_input', type=str,help="input type",
    #                     required=False, default="SIE")
    # parser.add_argument('--output_fname', type=str,help="output file name",
    #                     required=False, default="adega_input.csv")
    args = parser.parse_args()

    return args

class ZipUtilities:
    def toZip(self, file, filename):
        self._toZip_root_path = file

        zip_file = ZipFile(filename, 'w')
        if os.path.isfile(file):
            zip_file.write(file)
        else:
            self.addFolderToZip(zip_file, file)
        zip_file.close()

    def addFolderToZip(self, zip_file, folder): 
        for file in os.listdir(folder):
            full_path = os.path.join(folder, file)

            if str(full_path) == str(zip_file.filename):
                continue
            
            if os.path.isfile(full_path):
                rel_path = os.path.relpath(full_path, self._toZip_root_path)
                zip_file.write(full_path, rel_path)
            elif os.path.isdir(full_path):
                self.addFolderToZip(zip_file, full_path)

def main(submission_path, zip_path):
    '''
    Create a zip file with the summary of json analysis
    '''
    admission_csv_path = os.path.join(submission_path,"admission.csv")
    course_csv_path = os.path.join(submission_path,"course.csv")
    student_csv_path = os.path.join(submission_path,"student.csv")

    admission = AdmissionConversor(submission_path)
    data_admission,header_admission = admission.get_admission_as_matrix()
    df_admission = pd.DataFrame(data_admission)
    df_admission.columns = header_admission
    df_admission.to_csv(admission_csv_path, index=False)
    # print(df[["Ano","Período","students_per_semester_StudentsCount_2015_1o. Semestre"]])
    # print(df[["Ano","Período","ira_per_semester_std_2013_1o. Semestre"]])

    course = CourseConversor(submission_path)
    data_course,header_course = course.get_course_as_matrix()
    df_course = pd.DataFrame(data_course)
    df_course.columns = header_course
    df_course.to_csv(course_csv_path, index=False)
    # print(df[["Código","Nome","aprovacao_semestral_QuantidadeAprovacao_2015_1o. Semestre"]])
    # print(df[["Código","Nome","grafico_qtd_cursada_aprov_QuantidadeDeVezesCursadaAteAprovacao_1"]])
    # print(df[["Código","Nome","grafico_qtd_cursada_aprov_QuantidadeDeVezesCursadaAteAprovacao_2"]])
    # print(df[["Código","Nome","grafico_qtd_cursada_aprov_QuantidadeDeVezesCursadaAteAprovacao_MaisQue4"]])

    student = StudentConversor(submission_path)
    data_student,header_student = student.get_student_as_matrix()
    df_student = pd.DataFrame(data_student)
    df_student.columns = header_student
    df_student.to_csv(student_csv_path, index=False)
    
    # print(df[["Código","Nome","aprovacao_semestral_QuantidadeAprovacao_2015_1o. Semestre"]])
    # print(df[["Código","Nome","grafico_qtd_cursada_aprov_QuantidadeDeVezesCursadaAteAprovacao_1"]])
    # print(df[["Código","Nome","grafico_qtd_cursada_aprov_QuantidadeDeVezesCursadaAteAprovacao_2"]])
    # print(df[["Código","Nome","grafico_qtd_cursada_aprov_QuantidadeDeVezesCursadaAteAprovacao_MaisQue4"]])
    
    # zipObj = ZipFile(zip_path, 'w')
    # zipObj.write(admission_csv_path, os.path.basename(admission_csv_path))
    # zipObj.write(course_csv_path, os.path.basename(course_csv_path))
    # zipObj.write(student_csv_path, os.path.basename(student_csv_path))

    # zipObj.write(submission_path, os.path.basename(submission_path))
    
    # close the Zip File
    # zipObj.close()
    
    
    ZipUtilities().toZip(submission_path,zip_path)

    

if __name__ == '__main__':
    args = get_args()
    submission_path = args.input
    submission_path = args.zip_path

    main(submission_path)
    #teste da funcao create_csv
    #lista = ['coluna1','coluna70','coluna22','coluna42']
    #create_csv('testeDaFuncao.csv', lista, 7)
