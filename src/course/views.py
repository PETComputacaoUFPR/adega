from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from django.contrib import messages

from degree.models import Degree
from report_api.views import get_list_courses, get_course_detail
from uploads.models import Submission


def detail(request, submission_id, codigo_disciplina):
    submission_id = int(submission_id)
    submission = Submission.objects.get(id=submission_id)
    degree = submission.degree
    if not (degree in request.user.educator.degree.all()):
        return redirect("adega:dashboard")

    course_detail = get_course_detail(request.session, degree, codigo_disciplina)
    
    return render(request, 'course/detail.html',{
        "analysis_result": course_detail,
        "degree": degree,
        "submission": submission,
        "codigo_disciplina": codigo_disciplina,
        "nome_disciplina": course_detail["disciplina_nome"]
    })


def index(request, submission_id):
    submission_id = int(submission_id)
    submission = Submission.objects.get(id=submission_id)
    degree = submission.degree

    if not (degree in request.user.educator.degree.all()):
        return redirect("adega:dashboard")

    analysis_result = get_list_courses(request.session, degree)
    courses_list = analysis_result["cache"]
    code_to_name = analysis_result["disciplinas"]
    for code in courses_list:
        courses_list[code]["name"] = code_to_name[code]
    
    return render(request, 'course/index.html', {
        "courses": courses_list,
        "submission": submission
    })
