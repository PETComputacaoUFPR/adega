from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import logout as process_logout
from report_api.views import get_degree_information
from degree.models import Degree
from submission.models import Submission
import json
from guardian.decorators import permission_required_or_403

@permission_required_or_403('view_degree', (Submission, 'id', 'submission_id'))
def index(request, submission_id):
    submission_id = int(submission_id)

    submission = Submission.objects.get(id=submission_id)

    degree = submission.degree


    degree_data = get_degree_information(request.session, degree, submission_id=submission_id)
    return render(request, "degree/index.html", {
        "submission": submission,
        "degree": degree,
        "degree_data": degree_data
    })

