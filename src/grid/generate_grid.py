import pandas as pd
import numpy as np
from grid.models import Grid #, GridCourse, GridPeriod


def create_periods(disciplinas, grid):
    periods = {}
    for index,i in disciplinas.drop_duplicates("PERIODO_IDEAL").iterrows():
        period = GridPeriod.objects.create(grid=grid, number=i.PERIODO_IDEAL)
        periods[str(i.PERIODO_IDEAL)] = period
    return periods

def create_courses(disciplinas,periods, grid):
    course_list = disciplinas.drop_duplicates("COD_DISCIPLINA")
    courses = {}
    # create courses
    for index, i in course_list.iterrows():
        if i.DESCR_ESTRUTURA != "optativas":
            course = GridCourse.objects.create(name=i.NOME_DISCIPLINA,
                                               _type="Obrigatórias",
                                               code=i.COD_DISCIPLINA,
                                               period=periods[str(i.PERIODO_IDEAL)])
        else:
            course = GridCourse.objects.create(name=i.NOME_DISCIPLINA,
                                               _type="optativas",
                                               code=i.COD_DISCIPLINA,
                                               grid=grid)
        courses[i.COD_DISCIPLINA] = course
    # add prerequisites
#    prerequisites = disciplinas.groupby(["COD_DISCIPLINA"])
#    for j in prerequisites:
#        course = courses[j[0]]
#        print(course)
#        for k in j[1].drop_duplicates("COD_PRE_REQ"):
#            courses[k].prerequisites_set.add(course)
#            #course.prerequisites_set.add(courses[k.COD_DISCIPLINA])
#


def generate_grid(grid, debug):
    disciplinas = pd.read_excel(grid.path()+"/disciplinas.xls",
                                encoding='ISO-8859-1')
    equivalencias = pd.read_excel(grid.path()+"/equivalencias.xls",
                                  encoding='ISO-8859-1')

    periods = create_periods(disciplinas, grid)

    courses = create_courses(disciplinas, periods, grid)
    return True
