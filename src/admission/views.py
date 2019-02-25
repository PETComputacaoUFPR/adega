from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from django.contrib import messages

from degree.models import Degree
from report_api.views import get_list_admission, get_admission_detail
from submission.models import Submission
from guardian.decorators import permission_required_or_403


@permission_required_or_403('view_admission', (Submission, 'id', 'submission_id'))
def detail(request, submission_id, ano, semestre):
    submission_id = int(submission_id)
    submission = Submission.objects.get(id=submission_id)
    degree = submission.degree

    if not (degree in request.user.educator.degree.all()):
        return redirect("adega:dashboard")
    
    
    for admission in get_list_admission(request.session, degree, submission_id):
        if(admission["ano"] == ano and admission["semestre"] == semestre):
            admission_info = admission
            break
    
    admission_detail = get_admission_detail(
        request.session,
        degree,
        ano,
        semestre,
        submission_id
    )

    for x in admission_detail:
        admission_info[x] = admission_detail[x]

    if(admission_info["formatura_media"] == -1):
        admission_info["formatura_media"] = "Não há alunos formados nesta turma"
    
    return render(request, 'admission/detail.html',{
        "degree": degree,
        "admission_info": admission_info,
        "submission": submission
    })


@permission_required_or_403('view_admission', (Submission, 'id', 'submission_id'))
def index(request, submission_id):
    submission_id = int(submission_id)
    submission = Submission.objects.get(id=submission_id)
    degree = submission.degree

    if not (degree in request.user.educator.degree.all()):
        return redirect("adega:dashboard")

    return render(request, 'admission/index.html', {
        "listage_admissions": get_list_admission(
            request.session,
            degree,
            submission_id
        ),
        "degree": degree,
        "submission": submission
    })
