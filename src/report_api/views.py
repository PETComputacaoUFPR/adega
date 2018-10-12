from degree.models import Degree
from uploads.models import Submission
import json

def get_data(session,degree,data_name): 
    if "submission" in session:
        submission = session["submission"] 
    else:
        submission = Submission.objects.filter(degree=degree).last() 

    path_data = submission.path() + "/" + data_name 
    with open(path_data) as data_f:
        data = json.load(data_f) 
    return data

def get_degree_information(session, degree):
    return get_data(session,degree,"degree.json")

def get_list_admission(session, degree):
    return get_data(session,degree,"admission/lista_turma_ingresso.json")

def get_list_courses(session, degree):
    return get_data(session,degree,"disciplina/disciplinas.json")

def get_course_detail(session, degree, course_id):
    return get_data(session,degree,"disciplina/"+course_id+".json")

def get_list_students(session, degree, list_name):
    return get_data(session,degree,"students/list/"+list_name+".json")

def get_student_detail(session, degree, student_id):
    return get_data(session,degree,"students/"+student_id+".json")