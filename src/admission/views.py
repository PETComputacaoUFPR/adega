from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from django.contrib import messages

from degree.models import Degree
from report_api.views import get_list_admission



def detail(request, degree_id, ano, semestre):
    degree = Degree.objects.get(code=degree_id)
    if not (degree in request.user.educator.degree.all()):
        return redirect("adega:dashboard")
    
    
    for admission in get_list_admission(request.session, degree):
        if(admission["ano"] == ano and admission["semestre"] == semestre):
            admission_info = admission
            break

    return render(request, 'admission/detail.html',{
        "degree": degree,
        "admission_info": admission_info
    })


def index(request, degree_id):
    degree = Degree.objects.get(code=degree_id)
    if not (degree in request.user.educator.degree.all()):
        return redirect("adega:dashboard")

    return render(request, 'admission/index.html', {
        "listage_admissions": get_list_admission(request.session, degree),
        "degree": degree
    })
