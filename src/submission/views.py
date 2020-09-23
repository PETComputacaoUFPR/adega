from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from submission.models import Submission
from submission.forms import SubmissionForm
from degree.models import Degree
from submission.analysis import main as submission_analysis
from educator.models import Educator
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q

from guardian.decorators import permission_required_or_403

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404
from django.utils.text import slugify
import os
import urllib.parse

def download(request, submission_id):
    submission_id = int(submission_id)
    submission = Submission.objects.get(id=submission_id)

    if not submission.download_allowed(request.user):
        raise PermissionDenied

    file_path = submission.zip_path()
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(),
                content_type='application/zip charset=utf-8')
            
            content_disposition =  \
                "attachment; " \
                "filename={ascii_filename};" \
                "filename*=UTF-8''{utf_filename}".format(
                    ascii_filename=slugify(os.path.basename(file_path)),
                    utf_filename=urllib.parse.quote(
                        os.path.basename(file_path).encode("utf-8")))
            response['Content-Disposition'] = content_disposition
            return response
    raise Http404

@method_decorator(login_required, name='dispatch')
class SubmissionCreate(SuccessMessageMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = 'submission_create.html'
    success_url = reverse_lazy('dashboard')
    success_message = "Relatório enviado com suceso"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context["users"] = User.objects.filter(~Q(username=user.username))
        context["permissions"] = [x[1] for x in Submission._meta.permissions]
        context["perms"] = [x[0] for x in Submission._meta.permissions]
        context["hide_navbar"] = True
        context["degree_options"] = user.educator.degree.all()

        return context

    def form_valid(self, form):
        # muda nomes dos arquivos
        if ".csv" in form.instance.csv_data_file.name:
            form.instance.csv_data_file.name = "csv_data_file.csv"

        # adiciona a form.instance.usuario e curso
        form.instance.author = self.request.user.educator
        degree = Degree.objects.get(code=form.instance.degree.code)
        form.instance.degree = degree

        response = super(SubmissionCreate, self).form_valid(form)

        # trata permissoes
        data = self.request.POST.copy()
        users = {}
        for i in data.keys():
            # gets only permission data
            if i.startswith("perm-"):
                perm_str = i.split('-')
                # cache user
                if perm_str[1] not in users:
                    users[perm_str[1]] = User.objects.get(username=perm_str[1])

                # assing permission perm_str[2] to user perm_str[1] for
                # submission self.object
                assign_perm(perm_str[2], users[perm_str[1]], self.object)

        # assing all permission for self user
        for perm in Submission._meta.permissions:
            assign_perm(perm[0], self.request.user, self.object)

        submission_analysis.analyze(self.object, debug=False)

        return response


@method_decorator(login_required, name='dispatch')
class SubmissionUpdate(UpdateView):
    model = Submission
    template_name = 'submission_update.html'
    context_object_name = 'submission'
    success_url = reverse_lazy('dashboard')
    fields = [
        'csv_data_file',
        'relative_year',
        'relative_semester',
        'semester_status']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hide_navbar"] = True
        return context


@method_decorator(login_required, name='dispatch')
class SubmissionDelete(DeleteView):
    model = Submission
    template_name = 'submission_delete.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hide_navbar"] = True
        return context


@method_decorator(login_required, name='dispatch')
class SubmissionList(ListView):
    model = Submission
    template_name = 'submission_list.html'
    context_object_name = 'submission'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hide_navbar"] = True
        # context["degree_id"] = self.kwargs["degree_id"]
        return context

    def get_queryset(self):
        educator = self.request.user.educator
        # If this filter is changed, the download permission must be verified
        return self.model.objects.filter(author=educator)


@method_decorator(login_required, name='dispatch')
class SubmissionDetail(DetailView):
    model = Submission
    template_name = 'submission_detail.html'
    context_object_name = 'submission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hide_navbar"] = True
        return context
