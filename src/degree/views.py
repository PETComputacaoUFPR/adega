from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import logout as process_logout
from report_api.views import get_degree_information, get_list_students, get_student_detail, get_list_courses
from degree.models import Degree
from submission.models import Submission
import json
from student.grid import DegreeGrid

from guardian.decorators import permission_required_or_403

from submission.analysis.utils.situations import Situation
situations_pass = Situation.SITUATION_PASS
situations_pass = [Situation.code_to_str(c) for c in situations_pass]

situations_fail = Situation.SITUATION_FAIL
situations_fail = [Situation.code_to_str(c) for c in situations_fail]

@permission_required_or_403('view_degree', (Submission, 'id', 'submission_id'))
def index(request, submission_id):
    submission_id = int(submission_id)

    submission = Submission.objects.get(id=submission_id)

    degree = submission.degree
    degree_data = get_degree_information(request.session, degree, submission_id=submission_id)
    
    analysis_result = get_list_courses(request.session, degree, submission_id)
    courses_list = analysis_result["cache"]

    dg_list_context = []
    # dg = DegreeGrid(DegreeGrid.bcc_grid_2011)
    dg_list = DegreeGrid.get_degree_grid_list(degree.code)
    for dg in dg_list:
        dg = DegreeGrid(dg)
        grid_info = dg.get_degree_situation(courses_list)
        
        prerequisites = dg.grid_detail.prerequisites
        prerequisites_rev = {}
        for c1 in prerequisites:
            for c2 in prerequisites[c1]:
                if not (c2 in prerequisites_rev):
                    prerequisites_rev[c2] = []
                prerequisites_rev[c2].append(c1)


        dg_list_context.append({
            "grid_info": grid_info,
            "prerequisites": prerequisites,
            "prerequisites_rev": prerequisites_rev,
            "version": dg.grid_detail.version
        })
    
    return render(request, "degree/index.html", {
        "submission": submission,
        "degree": degree,
        "degree_data": degree_data,
        "situations_pass": situations_pass,
        "situations_fail": situations_fail,
        "dg_list": dg_list_context
    })

