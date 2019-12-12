from django.shortcuts import render
import json
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib.auth.decorators import login_required
from grid.models import Grid # , GridCourse, GridPeriod
from degree.models import Degree
from grid.forms import GridForm
from grid.generate_grid import generate_grid

from django.urls import reverse
from django.shortcuts import redirect

from student.grid import DegreeGrid

def create_course_from_json(json_data, degree_code):
    grid_version = json_data["version"]
    courses = {}
    print(json_data)

    periods = json_data["courses"].keys()
    periods = [int(x) for x in periods]

    for period in json_data["courses"].keys():
        for course in json_data["courses"][period]:
            course["course_period"] = int(course["course_period"])
            courses[course["course_code"]] = course
            
    courses_codes = list(courses.keys())
    courses_codes_set = set(courses_codes)
    
    __import__('pprint').pprint(courses)
    
    # Validation
    for code in courses:
        eq = courses[code]["course_equivalent"].split(",")
        eq = [x for x in eq if x != '']
        # if len(set(eq) - courses_codes_set) > 0:
        #     return None
        courses[code]["course_equivalent"] = eq
        
        req = courses[code]["course_prerequisite"].split(",")
        req = [x for x in req if x != '']

        if len(set(req) - courses_codes_set) > 0:
            print(req)
            print(set(req) - courses_codes_set)
            print(len(set(req) - courses_codes_set))
            return None
        courses[code]["course_prerequisite"] = req
    
    dg = Degree.objects.get(code=degree_code)
    grid_desc_dict = {
        "version": grid_version,
        "grid": [[] for i in range(len(periods))],
        "repeated_codes": [],
        "fake_codes": [],
        "code_to_name": {},
        "equiv_codes": {},
        "prerequisites": {},
        "phases": {}
    }
    
    for code in courses:
        course = courses[code]
        period = course["course_period"]

        grid_desc_dict["grid"][period-1].append(code)
        grid_desc_dict["code_to_name"][code] = course["course_name"]
        grid_desc_dict["equiv_codes"][code] = course["course_equivalent"]
        grid_desc_dict["prerequisites"][code] = course["course_prerequisite"]

        if courses_codes.count(code) > 1:
            grid_desc_dict["repeated_codes"].append(code)
        if course["course_type"] != "Obrigatória":
            grid_desc_dict["fake_codes"].append(code)

    print(grid_desc_dict)
        
    new_grid = Grid(degree=dg, version=grid_version,
                    data_as_string=json.dumps(grid_desc_dict))

    # periods = list(set)
    # Prevent loop dependencies
    # i = 0
    # prior_queue = list(courses_codes)
    # courses_instances = {}
    # while(len(prior_queue) > 0):
    #     course = prior_queue[i]
    #     eq = course["course_equivalent"]
    #     req = course["course_prerequisite"]
    #     # Check if all equivalences and pre requisites was already instanced
    #     courses_instances_set = set(courses_instances.keys())
    #     remain_eq = len(set(eq) - courses_instances_set)
    #     remain_req = len(set(req) - courses_instances_set)
    #     if remain_eq == 0 and  remain_req == 0:
    #         new_course = GridCourse(
    #             # name=course["course_name"],
    #             # _type=course["course_type"],
    #             # code=course["course_code"]
    #         )
    
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


# class GridUpdate(UpdateView):
#     model = Grid


class GridDelete(DeleteView):
    model = Grid
    template_name = 'grid_delete.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hide_navbar"] = True
        degree_code = self.kwargs["degree_code"]
        return context


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
        if new_grid is None:
            return HttpResponseBadRequest()
        
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
