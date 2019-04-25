from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import logout as process_logout
from report_api.views import get_degree_information
from degree.models import Degree
from submission.models import Submission
import json
from guardian.decorators import permission_required_or_403

@permission_required_or_403('view_cepe9615', (Submission, 'id', 'submission_id'))
def index(request, submission_id):
    submission_id = int(submission_id)

    submission = Submission.objects.get(id=submission_id)
    degree = submission.degree

    if not (degree in request.user.educator.degree.all()):
        return redirect("adega:dashboard")

    cepe9615_data = get_cepe9615_information(request.session,degree, submission_id=submission_id)

    last_semester = (submission.relative_semester - 1)
    if (last_semester == 0):
        year = str(submission.relative_year - 1)
        semester = "2"
    else:
        year = str(submission.relative_year)
        semester = str(last_semester)
    year_semester = "(" + year + ", '" + semester + "o. Semestre')"
    analysys_result = {'alunos_mais_que_x_reprovacoes_na_mesma_disciplina': cepe9615_data['student_fails_course'],
                        'alunos_mais_que_x_reprovacoes_em_duas_ou_mais_disciplinas_distintas': cepe9615_data['student_fails_2_courses'],
                        'alunos_mais_que_x_reprovacoes_na_mesma_disciplina_por_freq': cepe9615_data['fails_by_freq'],
                        'alunos_que_reprovaram_em_x_materias_no_semestre': cepe9615_data['fails_semester'],
                        'alunos_que_reprovaram_por_falta_em_todas_as_materias_do_semestre': cepe9615_data['fails_by_freq_semester'],
    }

    return render(request,"cepe9615/index.html",{
        "submission":submission,
        'analysys_result': analysys_result,
        'year_semester': year_semester
    })