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

from django.contrib.admin.utils import flatten
from django.http import HttpResponse

def check_keys(grid_as_dict):

    # Checa se todos os códigos estão presentes
    # e retorna as chaves inválidas, se houver
    keys_error = []
    
    keys = ["version",
            "grid",
            "repeated_codes",
            "fake_codes",
            "code_to_name",
            "equiv_codes",
            "prerequisites",
            "phases"]
    
    keys_to_displayname = {
        "version": "Versão",
        "grid": "Grade",
        "repeated_codes": "Lista de códigos repetidos",
        "fake_codes": "Códigos falsos",
        "code_to_name": "Nomes de disciplinas",
        "equiv_codes": "Lista de códigos equivalentes",
        "prerequisites": "Lista de pré-requisitos",
        "phases": "Fases do curso"
    }
    for item in keys:
        if item not in grid_as_dict:
            keys_error.append(item)
    
    if len(keys_error) > 0:
        msg_error = ("Houve algum erro durante a construção da grade. "
                     "Verifique se os seguintes itens estão corretos: ")
        
        keys_error_displayname = [keys_to_displayname[x] for x in keys_error]
        keys_error_str = "; ".join(keys_error_displayname)
        return msg_error + keys_error_str
    else:
        return None
    

def check_version(grid_as_dict):

    # Se for enviado como json, seria necessário checar a versão
    # Checa se a versão da grade está no json
    is_empty = not bool(grid_as_dict['version'])

    version_error = ""

    if is_empty:
        version_error = "Por favor, cheque se o campo do nome da versão foi preenchido. "
        return version_error
    else:
        return None

def check_repeated(grid_as_dict):

    # Identifica os repetidos em grid
    all_codes = []
    list_repeated_codes = []

    for code in flatten(grid_as_dict['grid']):
        if not code in all_codes:
            all_codes.append(code)
        else:
            list_repeated_codes.append(code)
    
    # Checa se todos os códigos repetidos estão no repeated_codes
    # Se não estiver, será adicionado
    for repeated_item in set(list_repeated_codes):
        if repeated_item not in grid_as_dict['repeated_codes']:
            grid_as_dict['repeated_codes'].append(repeated_item)

    return all_codes

def check_phase_code(grid_as_dict, all_codes):

    phase_errors = []

    # Checa se as disciplinas das fases estão na grid
    for phase_codes in flatten(grid_as_dict['phases'].values()):
        if phase_codes not in all_codes:
            phase_errors.append(phase_codes)
    
    if len(phase_errors) > 0:
        msg_error = "Por favor, cheque se os seguintes códigos são válidos: "
        phase_error_str = ",".join(phase_errors)
        return msg_error + phase_error_str
    else:
        return None

def check_course_from_json(grid_as_dict):
    errors = []

    try:
        all_codes = check_repeated(grid_as_dict)
    except:
        errors.append("Um erro inesperado aconteceu durante a verificação da grade e dos códigos repetidos")
        all_codes = None

    try:
        keys_error_list = check_keys(grid_as_dict)
        if not keys_error_list is None:
            errors.append(keys_error_list)
    except:
        errors.append("Um erro inesperado aconteceu durante a verificação dos campos")
    
    try:
        version_error_list = check_version(grid_as_dict)
        if not version_error_list is None:
            errors.append(version_error_list)
    except:
        errors.append("Um erro inesperado aconteceu durante a verificação do nome da versão")

    if not all_codes is None:
        try:
            phase_code_error_list = check_phase_code(grid_as_dict, all_codes)
            if not phase_code_error_list is None:
                errors.append(phase_code_error_list)
        except:
            errors.append("Um erro inesperado aconteceu durante a verificação das fases da grade")

    return errors


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
        degree_code = kwargs["degree_code"]

        grid_as_json_string = request.POST.copy()["grid"]

        grid_as_dict = json.loads(grid_as_json_string)

        grid_as_json_string = json.dumps(grid_as_dict, indent=4, sort_keys=True)

        error_list = check_course_from_json(grid_as_dict)

        grid_version = grid_as_dict["version"]
        dg = Degree.objects.get(code=degree_code)

        if Grid.objects.filter(degree=dg, version=grid_version).exists():
            error_list.append("Já existe uma versão com esse nome associada no banco de dados")
        
        if len(grid_version) > 40:
            error_list.append("O nome da versão deve conter 40 caracteres ou menos")

        if len(error_list) > 0:
            context = {
                'status': '400', 'reason': error_list
            }
            response = HttpResponse(json.dumps(context,ensure_ascii=False).encode("utf8"),
                                    content_type='application/json')
            response.status_code = 400
            return response
        

        
        new_grid = Grid(degree=dg, version=grid_version,
                        data_as_string=grid_as_json_string)
        new_grid.save()

        return redirect('/grid/{}'.format(degree_code))


        '''
        grid = json.loads(grid_json)
        new_grid = create_course_from_json(grid,degree_code)
        if new_grid is None:
            return HttpResponseBadRequest()
        
        # return HttpResponseRedirect(self.success_url)
        return redirect('/grid/{}'.format(degree_code))
        # return HttpResponseRedirect(reverse('grids', args=[degree_code]))
        '''

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
        # user = self.request.user
        context = super().get_context_data(**kwargs)
        context["hide_navbar"] = True
        context["degree_code"] = Degree.objects.get(code=self.kwargs["degree_code"])
        # print(self.kwargs)
        return context
