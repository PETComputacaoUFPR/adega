from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from django.contrib import messages

from degree.models import Degree
from report_api.views import get_list_admission



def detail(request, degree_id, ano, semestre):
    degree = Degree.objects.get(code=degree_id)
    if not (degree in request.user.educator.degree.all()):
        return redirect("adega:dashboard")
    
    return render(request, 'admission/detail.html',{
        "degree": degree
    })


def index(request, degree_id):
    degree = Degree.objects.get(code=degree_id)
    if not (degree in request.user.educator.degree.all()):
        return redirect("adega:dashboard")

    return render(request, 'admission/index.html', {
        "listage_admissions": get_list_admission(request.session, degree),
        "degree": degree
    })
