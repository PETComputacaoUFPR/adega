from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, UpdateView, DeleteView
from django.contrib.auth import logout as process_logout
from django.views.generic import ListView, DetailView
from report_api.views import get_degree_information
from degree.models import Degree, Grid
from submission.models import Submission
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
import json
from guardian.decorators import permission_required_or_403
from degree.forms import GridForm
from django.urls import reverse_lazy


@method_decorator(login_required, name='dispatch')
class GridCreate(SuccessMessageMixin, CreateView):
    model = Grid
    form_class = GridForm
    template_name = 'grid_create.html'
    success_url = reverse_lazy('dashboard')
    success_message = "Matriz curricular enviada com sucesso"

    def form_valid(self, form):
        form.instance.disciplinas.name = "disciplinas.xls"
        form.instance.prerequisitos.name = "prerequisitos.xls"
        form.instance.author = self.request.user.educator
        degree = Degree.objects.get(code=form.instance.degree.code)
        form.instance.degree = degree
        response = super(SubmissionCreate, self).form_valid(form)



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

