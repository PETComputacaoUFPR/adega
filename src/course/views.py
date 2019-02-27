from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from django.contrib import messages

from degree.models import Degree
from report_api.views import get_list_courses, get_course_detail
from submission.models import Submission
from guardian.decorators import permission_required_or_403


@permission_required_or_403('view_course', (Submission, 'id', 'submission_id'))
def detail(request, submission_id, codigo_disciplina):
    submission_id = int(submission_id)
    submission = Submission.objects.get(id=submission_id)
    degree = submission.degree

    course_detail = get_course_detail(
        request.session,
        degree,
        codigo_disciplina,
        submission_id
    )
    
    return render(request, 'course/detail.html',{
        "analysis_result": course_detail,
        "degree": degree,
        "submission": submission,
        "codigo_disciplina": codigo_disciplina,
        "nome_disciplina": course_detail["disciplina_nome"]
    })


@permission_required_or_403('view_course', (Submission, 'id', 'submission_id'))
def index(request, submission_id):
    submission_id = int(submission_id)
    submission = Submission.objects.get(id=submission_id)
    degree = submission.degree


    analysis_result = get_list_courses(request.session, degree, submission_id)
    courses_list = analysis_result["cache"]
    code_to_name = analysis_result["disciplinas"]
    for code in courses_list:
        courses_list[code]["name"] = code_to_name[code]
    
    return render(request, 'course/index.html', {
        "courses": courses_list,
        "submission": submission
    })

def compare(request, submission_id):
    print(request,submission_id)
    submission_id = int(submission_id)
    print(submission_id)

    submission = Submission.objects.get(id=submission_id)
    degree = submission.degree

    if not (degree in request.user.educator.degree.all()):
        return redirect("adega:dashboard")

    analysis_result = get_list_courses(request.session, degree, submission_id)
    courses_list = analysis_result["cache"]
    code_to_name = analysis_result["disciplinas"]
    
    # TODO: The data of one graph is in another file (detail file)
    # The analysis must be changed to join the information.
    # Even if the data is redundant
    
    charts = {
        "compara_aprov": analysis_result["compara_aprov"]
    }
    
    chart_approvation_rate = {}
    for course_name in courses_list:
        course_detail = get_course_detail(request.session, degree, course_name, submission_id)
        chart_approvation_rate[course_name] = course_detail["aprovacao_semestral"]
    
    charts["approvation_rate"] = chart_approvation_rate

    courses_info = {}
    course_names = {}
    for code in courses_list:
        courses_list[code]["name"] = code_to_name[code]
        course_names[code] = courses_list[code]["name"]
        
        courses_info[code] = {
            "grade_mean": courses_list[code]["nota"],
            "fail_rate": courses_list[code]["taxa_reprovacao_absoluta"],
            "fail_rate_presence": courses_list[code]["taxa_reprovacao_frequencia"],
            "lock_rate": courses_list[code]["taxa_trancamento"]
        }

    return render(request, 'course/compare.html', {
        "charts": charts,
        "submission": submission,
        "course_names": course_names,
        "courses_info": courses_info,
    })
