from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as process_logout
from submission.models import Submission




@login_required
def dashboard(request):
    degrees = request.user.educator.degree.all()
    degrees_last_submissions = []
    for degree in degrees:
        last_submission = Submission.objects.filter(
            degree=degree
        ).last()
        if not (last_submission is None):
            degrees_last_submissions.append({
                "name": degree.name,
                "code": degree.code,
                "last_submission": last_submission
            })
    return render(request, 'adega/dashboard.html', {"title": "Dashboard",
                                                    "degrees_last_submissions":degrees_last_submissions,
                                                    "hide_navbar": True
                                                    })


@login_required
def logout(request):
    process_logout(request)

    return redirect('public:index')
