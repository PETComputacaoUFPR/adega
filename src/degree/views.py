from django.shortcuts import render, redirect
from django.views.generic import view
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as process_logout

# Create your views here.

@login_required
def setDegree(request,degree_id):
    request.session["degree"] = degree_id 
    return redirect('public:index' ) 

@login_required
def Degreeindex(request):
    if(!("degree" in request.session)):
        return redirect('dashboard') 

class Views(view):
    template_name = "index.html" 
    @login_required
    def setDegree(self,request,degree_id):
        request.session["degree" ] = degree_id 
        return redirect('degree:index' ) 
    def index(self,request):
        degree = Degree.objects.get(code = request.session["degree"]) 
        submission = degree.submission
        if (("submission" in request.session)):
            submission = request.session["submission"] 
            submission = Submission.objects.get(id = submission) 
        
         degree_path = submission.path()  
         with open(submission.path()) as File:

