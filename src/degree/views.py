from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as process_logout
from degree.models import * 

# Create your views here.

@login_required
def index(request,degree_id):
    degree = Degree.objects.get(code=degree_id) 
    return render(request,"degree/index.html",{"degree":degree}) 
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
