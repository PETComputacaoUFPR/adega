from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from django.contrib import messages

from degree.models import Degree
from report_api.views import get_list_students, get_student_detail

import json


def detail(request, degree_id, grr):
    degree = Degree.objects.get(code=degree_id)
    if not (degree in request.user.educator.degree.all()):
        return redirect("adega:dashboard")

    


    
    cache_j = get_student_detail(request.session, degree, grr)


    analysis_result = {
        'indice_aprovacao' : cache_j['taxa_aprovacao'],
        'periodo_real': cache_j['periodo_real'],
        'periodo_pretendido': cache_j['periodo_pretendido'],
        'ira_semestral': json.dumps(cache_j['ira_semestral']),
        'indice_aprovacao_semestral': cache_j['indice_aprovacao_semestral'],
        # 'posicao_turmaIngresso_semestral': json.dumps(sorted(cache_j['posicao_turmaIngresso_semestral'].items())),
        'ira_por_quantidade_disciplinas': json.dumps(cache_j['ira_por_quantidade_disciplinas']),
        'student': cache_j['student'],
        'aluno_turmas': cache_j["aluno_turmas"],
    }

    return render(request, 'student/detail.html', {
        'degree_id': degree_id,
        'analysis_result': analysis_result
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

