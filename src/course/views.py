from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from django.contrib import messages

from degree.models import Degree
from report_api.views import get_list_courses, get_course_detail



def detail(request, degree_id, codigo_disciplina):
    degree = Degree.objects.get(code=degree_id)
    if not (degree in request.user.educator.degree.all()):
        return redirect("adega:dashboard")

    course_detail = get_course_detail(request.session, degree, codigo_disciplina)
    
    return render(request, 'course/detail.html',{
        "analysis_result": course_detail,
        "degree": degree,
        "codigo_disciplina": codigo_disciplina,
        "nome_disciplina": course_detail["disciplina_nome"]
    })


def index(request, degree_id):
    degree = Degree.objects.get(code=degree_id)
    if not (degree in request.user.educator.degree.all()):
        return redirect("adega:dashboard")

    analysis_result = get_list_courses(request.session, degree)
    courses_list = analysis_result["cache"]

    return render(request, 'course/index.html', {
        "courses": courses_list,
        "degree": degree
    })
