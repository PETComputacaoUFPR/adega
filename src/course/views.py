from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
@login_required
def index(request, degree_id):
    pass

@login_required
def detail(request, degree_id, course_code):
    pass

@login_required
def compare(request, degree_id):
    pass
