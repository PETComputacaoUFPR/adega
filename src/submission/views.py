from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from submission.models import Submission
from submission.forms import SubmissionForm
from degree.models import Degree
from submission.analysis import main as submission_analysis
from multiprocessing import Process
from django.http import HttpResponseRedirect

class SubmissionCreate(SuccessMessageMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = 'submission_create.html'
    success_url = reverse_lazy('dashboard')
    success_message = "Relatório enviado com suceso"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hide_navbar"] = True
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

        #submission_analysis.analyze(self.object, debug=False)
        analysis = Process(target=submission_analysis.analyze, args=(self.object, False))
        analysis.start()

        #return response
        return HttpResponseRedirect('/adega/submission')


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

class SubmissionDelete(DeleteView):
    model = Submission
    template_name = 'submission_delete.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hide_navbar"] = True
        return context

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


class SubmissionDetail(DetailView):
    model = Submission
    template_name = 'submission_detail.html'
    context_object_name = 'submission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hide_navbar"] = True
        return context
