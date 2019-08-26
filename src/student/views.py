from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from django.contrib import messages

from degree.models import Degree
from report_api.views import get_list_students, get_student_detail

import json

from submission.models import Submission
from guardian.decorators import permission_required_or_403

from student.grid import DegreeGrid

from submission.analysis.utils.situations import Situation

situations_pass = Situation.SITUATION_PASS
situations_pass = [Situation.code_to_str(c) for c in situations_pass]

situations_fail = Situation.SITUATION_FAIL
situations_fail = [Situation.code_to_str(c) for c in situations_fail]

@permission_required_or_403('view_student', (Submission, 'id', 'submission_id'))
def detail(request, submission_id, grr):
    submission_id = int(submission_id)
    submission = Submission.objects.get(id=submission_id)
    degree = submission.degree

    cache_j = get_student_detail(
        request.session,
        degree,
        grr,
        submission_id
    )

    hist = cache_j["aluno_turmas"]
    dg = DegreeGrid(DegreeGrid.grid)
    grid_info, grid_info_extra = dg.get_situation(hist)
    
    analysis_result = {
        'indice_aprovacao' : cache_j['taxa_aprovacao'],
        'periodo_real': cache_j['periodo_real'],
        'periodo_pretendido': cache_j['periodo_pretendido'],
        'ira_semestral': json.dumps(cache_j['ira_semestral']),
        'indice_aprovacao_semestral': cache_j['indice_aprovacao_semestral'],
        'posicao_turmaIngresso_semestral': json.dumps(cache_j['posicao_turmaIngresso_semestral']),
        'ira_por_quantidade_disciplinas': json.dumps(cache_j['ira_por_quantidade_disciplinas']),
        'student': cache_j['student'],
        'aluno_turmas': hist,
        'grid': grid_info,
        'grid_extra': grid_info_extra
    }

    return render(request, 'student/detail.html', {
        'degree': degree,
        'analysis_result': analysis_result,
        "submission": submission,
        "situations_pass": situations_pass,
        "situations_fail": situations_fail,
    })



@permission_required_or_403('view_student', (Submission, 'id', 'submission_id'))
def index(request, submission_id):
    submission_id = int(submission_id)
    submission = Submission.objects.get(id=submission_id)
    degree = submission.degree



    sem_evasao = get_list_students(
        request.session,
        degree,
        "Sem evasão",
        submission_id
    )
    formatura = get_list_students(
        request.session,
        degree,
        "Formatura",
        submission_id
    )
    abandono = get_list_students(
        request.session,
        degree,
        "Abandono",
        submission_id
    )
    desistencia = get_list_students(
        request.session,
        degree,
        "Desistência",
        submission_id
    )
    outros = get_list_students(
        request.session,
        degree,
        "Outro",
        submission_id
    )

    return render(request, 'student/index.html', {
        'degree': degree,
        'formatura': formatura,
        'sem_evasao': sem_evasao,
        'abandono': abandono,
        'desistencia': desistencia,
        'outros': outros,
        "submission": submission,
        "situations_pass": situations_pass,
        "situations_fail": situations_fail,
    })

