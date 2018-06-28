from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from django.contrib import messages

from degree.models import Degree
from report_api.views import get_list_students, get_course_detail



def detail(request, degree_id, codigo_disciplina):
    degree = Degree.objects.get(code=degree_id)
    if not (degree in request.user.educator.degree.all()):
        return redirect("adega:dashboard")

    course_detail = get_course_detail(request.session, degree, codigo_disciplina)
    
    return render(request, 'student/detail.html',{
        "analysis_result": course_detail,
        "degree": degree,
        "codigo_disciplina": codigo_disciplina,
        "nome_disciplina": course_detail["disciplina_nome"]
    })


def index(request, degree_id):
    degree = Degree.objects.get(code=degree_id)
    if not (degree in request.user.educator.degree.all()):
        return redirect("adega:dashboard")


    sem_evasao = get_list_students(request.session, degree, "Sem evasão")
    formatura = get_list_students(request.session, degree, "Formatura")
    abandono = get_list_students(request.session, degree, "Abandono")
    desistencia = get_list_students(request.session, degree, "Desistência")
    outros = get_list_students(request.session, degree, "Outro")

    return render(request, 'student/index.html', {
        'degree': degree,
        'formatura': formatura,
        'sem_evasao': sem_evasao,
        'abandono': abandono,
        'desistencia': desistencia,
        'outros': outros
    })

