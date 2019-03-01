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
        form.instance.historico.name = "historico.xls"
        form.instance.matricula.name = "matricula.xls"
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
        'historico',
        'matricula',
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
