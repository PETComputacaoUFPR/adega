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

    course = CourseConversor(submission_path)
    data_course,header_course = course.get_course_as_matrix()
    df_course = pd.DataFrame(data_course)
    df_course.columns = header_course
    df_course.to_csv(course_csv_path, index=False)

    student = StudentConversor(submission_path)
    data_student,header_student = student.get_student_as_matrix()
    df_student = pd.DataFrame(data_student)
    df_student.columns = header_student
    df_student.to_csv(student_csv_path, index=False)
    
    
    ZipUtilities().toZip(submission_path,zip_path)

    

if __name__ == '__main__':
    args = get_args()
    submission_path = args.input
    submission_path = args.zip_path

    main(submission_path)