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

def get_degree_information(session,degree):
    return get_data(session,degree,"degree.json") 

