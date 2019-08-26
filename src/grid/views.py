#from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from grid.models import Grid, GridCourse, GridPeriod
from degree.models import Degree
from grid.forms import GridForm
from grid.generate_grid import generate_grid


class GridList(ListView):
    model = Grid
    template_name = 'grid_list.html'
    context_object_name = 'grids'
    degree = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hide_navbar"] = True
        context["degree"] = self.degree
        return context

    def get_queryset(self):
        self.degree = Degree.objects.get(code=self.kwargs["degree_code"])
        return self.model.objects.filter(degree=self.degree)


class GridDetail(DetailView):
    model = Grid
    template_name = 'grid_detail.html'
    context_object_name = 'grid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hide_navbar"] = True

        return context


class GridUpdate(UpdateView):
    model = Grid


class GridDelete(DeleteView):
    model = Grid


class GridCreate(CreateView):
    model = Grid
    template_name = 'grid_create.html'
    context_object_name = 'grid'
    success_url = reverse_lazy('dashboard')
    form_class = GridForm

    def form_valid(self, form):

        # muda nomes dos arquivos
        form.instance.disciplinas.name = "disciplinas.xls"
        form.instance.equivalencias.name = "equivalencias.xls"
        # adiciona a form.instance.usuario e curso
        form.instance.author = self.request.user.educator
        degree = Degree.objects.get(code=form.instance.degree.code)
        form.instance.degree = degree

        response = super(GridCreate, self).form_valid(form)

        print(generate_grid(self.object, debug=False))
        print(self.object)
        return response

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context["hide_navbar"] = True
        context["degree_options"] = user.educator.degree.all()
        return context
