from django.shortcuts import render
import json
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib.auth.decorators import login_required
from grid.models import Grid, GridCourse, GridPeriod
from degree.models import Degree
from grid.forms import GridForm
from grid.generate_grid import generate_grid

from django.urls import reverse
from django.shortcuts import redirect

def create_course_from_json(json_data, degree_code):
    grid_version = json_data["version"]
    courses = {}
    for period in json_data["courses"].keys():
        for course in json_data["courses"][period]:
            courses[course["course_code"]] = course
    __import__('pprint').pprint(courses)

    # course_codes = 
    dg = Degree.objects.get(code=degree_code)
    new_grid = Grid(degree=dg, version=grid_version)
    new_grid.save()
    return new_grid

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



class GridCreate(View):
    model = Grid
    template_name = 'grid_create.html'
    context_object_name = 'grid'
    success_url = reverse_lazy('dashboard')

    def post(self, request, *args, **kwargs):
        grid_json = request.POST.copy()["grid"]
        degree_code = kwargs["degree_code"]
        grid = json.loads(grid_json)
        new_grid = create_course_from_json(grid,degree_code)

        # return HttpResponseRedirect(self.success_url)
        return redirect('/grid/{}'.format(degree_code))
        # return HttpResponseRedirect(reverse('grids', args=[degree_code]))


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, kwargs)
    # para arquivos
    #def form_valid(self, form):

    #    # muda nomes dos arquivos
    #    form.instance.disciplinas.name = "disciplinas.xls"
    #    form.instance.equivalencias.name = "equivalencias.xls"
    #    # adiciona a form.instance.usuario e curso
    #    form.instance.author = self.request.user.educator
    #    degree = Degree.objects.get(code=form.instance.degree.code)
    #    form.instance.degree = degree

    #    response = super(GridCreate, self).form_valid(form)

    #    print(generate_grid(self.object, debug=False))
    #    print(self.object)
    #    return response

    def get_context_data(self, **kwargs):
        user = self.request.user
        #context = super().get_context_data(**kwargs)
        context["hide_navbar"] = True
        #context["degree"] = Degree.objects.get(code=self.kwargs["degree_code"])
        print(self.kwargs)
        return context
