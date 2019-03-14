from degree.models import Degree
from submission.models import Submission
import json

def get_data(session, degree, data_name, submission_id=None):
    if(submission_id):
        submission = Submission.objects.filter(id=submission_id).last()
    elif "submission" in session:
        submission = session["submission"]
    else:
        submission = Submission.objects.filter(degree=degree).last()

    path_data = submission.path() + "/" + data_name
    with open(path_data) as data_f:
        data = json.load(data_f)
    return data

def get_degree_information(session, degree, submission_id=None):
    return get_data(session,degree,"degree.json", submission_id=submission_id)

def get_list_admission(session, degree, submission_id=None):
    return get_data(session,degree,"admissions/lista_turma_ingresso.json", submission_id=submission_id)

def get_admission_detail(session, degree, year, semester, submission_id=None):
    return get_data(session,degree,"admissions/"+year+"/"+semester+".json", submission_id=submission_id)

def get_list_courses(session, degree, submission_id=None):
    return get_data(session,degree,"courses/disciplinas.json", submission_id=submission_id)

def get_course_detail(session, degree, course_id, submission_id=None):
    return get_data(session,degree,"courses/"+course_id+".json", submission_id=submission_id)

def get_list_students(session, degree, list_name, submission_id=None):
    return get_data(session,degree,"students/list/"+list_name+".json", submission_id=submission_id)

def get_student_detail(session, degree, student_id, submission_id=None):
    return get_data(session,degree,"students/"+student_id+".json", submission_id=submission_id)

def get_cepe9615_information(session, degree, submission_id=None):
    return get_data(session,degree,"cepe9615.json", submission_id=submission_id)
