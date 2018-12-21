from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as process_logout
from report_api.views import get_degree_information
from degree.models import Degree
from uploads.models import Submission
import json


@login_required
def index(request, submission_id):
    submission_id = int(submission_id)
    submission = Submission.objects.get(id=submission_id)
    degree = submission.degree


    if not (degree in request.user.educator.degree.all()):
        return redirect("adega:dashboard")

    degree_data = get_degree_information(request.session,degree, submission_id=submission_id)
    return render(request,"degree/index.html",{
        "submission":submission,
        "degree": degree,
        "degree_data":degree_data
    })

#class Views(View):
#    template_name = "index.html"
#    @login_required
#    def setDegree(self,request,degree_id):
#        request.session["degree"] = degree_id
#        return redirect('degree:index' )
#    def index(self,request):
#        if("degree" in request.session):
#            degree = Degree.objects.get(code = request.session["degree"])
#        else:
#            return redirect("adega:dashboard")
#        submission = degree.submission
#        return render(request,"degree/index",{"degree":degree})
#
#
