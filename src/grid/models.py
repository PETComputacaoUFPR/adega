from django.db import models
from degree.models import Degree
from os import path
from django.conf import settings

import json

def get_path(instance, filename):
    return '{}/{}/{}'.format(instance.degree.code, instance.id, filename)


class Grid(models.Model):
    # version = models.IntegerField()
    version = models.CharField(max_length=40)
    data_as_string = models.TextField()

    degree = models.ForeignKey(
            Degree,
            on_delete=models.CASCADE,
            related_name="grids",
            related_query_name="grids",
            )

    class Meta:
        unique_together = ('version', 'degree',)

    def __str__(self):
        return "Curso: {} Versão: {}".format(self.degree, self.version)

    # def get_courses(self):
    #     courses = {}
    #     for period in self.periods.all():
    #         for course in period.courses.all():
    #             courses[course.code] = course.name
    #     return courses

    # def get_periods(self):
    #     periods = []
    #     for period in self.periods.all():
    #         periods.append(period.get_courses())
    #     return periods

    # def get_equiv_code(self):
    #     equiv_code = {}
    #     for course in self.optatives.all():
    #         equiv_code[course.code] = ["OPT"]
    #     return equiv_code

    # def get_grid(self):
    #     grid = {"year": self.version,
    #             "grid": self.get_periods(),
    #             "repeated_codes": ["OPT"],
    #             "fake_codes": ["OPT", "TG I", "TG II"],
    #             "code_to_name": self.get_courses(),
    #             "equiv_codes": self.get_equiv_code()
    #             }
    #     return grid

#     #def save(self, *args, **kwargs):
#     #    """
#     #    Sobrescrita do metodo save.
#     #    É necesário rescrever o metodo save, para poder obter o id da instancia
#     #    enquanto o modelo ainda não foi salvo no banco de dados.

#     #    """
#     #    if self.id is None:
#     #        disciplinas = self.disciplinas
#     #        equivalencias = self.equivalencias
#     #        self.disciplinas = None
#     #        self.equivalencias = None
#     #        super(Grid, self).save(*args, **kwargs)
#     #        self.disciplinas = disciplinas
#     #        self.equivalencias = equivalencias
#     #        # kwargs.pop('force_insert')
#     #    super(Grid, self).save(*args, **kwargs)

#     def path(self):
#         return path.join(settings.MEDIA_ROOT, self.degree.code, str(self.id))


# class GridPeriod(models.Model):
#     number = models.IntegerField()
#     grid = models.ForeignKey(
#             Grid,
#             on_delete=models.CASCADE,
#             related_name="periods",
#             related_query_name="periods"
#             )

#     def get_courses(self):
#         courses = []
#         for course in self.courses.all():
#             courses.append(course.code)
#         return courses

#     def __str__(self):
#         return "Grade: {}-{}\n Periodo: {}\nDisciplinas:\n {}".format(self.grid.version,
#                                                                       self.grid.id,
#                                                                       self.number,
#                                                                       self.get_courses())


# class GridCourse(models.Model):
#     name = models.CharField(max_length=200)
#     _type = models.CharField(max_length=32)
#     code = models.CharField(max_length=32)
#     prerequisites = models.ForeignKey("self",related_name="pre_requisites",related_query_name="pre_requisites", blank=True, null=True,)
#     equivalency = models.ForeignKey("self",related_name="equiv", related_query_name="equiv", blank=True, null=True,)
#     # prerequisites = models.ManyToManyField("self", through="GridCourseRequisite",
#     #                                        symmetrical=False, )
#     # equivalences = models.ManyToManyField("self", through="GridCourseEquivalence",
#     #                                        symmetrical=True)
#     period = models.ForeignKey(
#             GridPeriod,
#             on_delete=models.CASCADE,
#             related_name="courses",
#             related_query_name="courses",
#             blank=True,
#             null=True,
#             )
#     grid = models.ForeignKey(
#             Grid,
#             on_delete=models.CASCADE,
#             related_name="optatives",
#             related_query_name="optatives",
#             blank=True,
#             null=True,
#             )

#     def __str__(self):
#         return "{} {}".format(self.name, self.code)

# class ContactRelationship(models.Model):
#     types = models.ManyToManyField('RelationshipType', blank=True,
#                                    related_name='contact_relationships')
#     from_contact = models.ForeignKey('Contact', related_name='from_contacts')
#     to_contact = models.ForeignKey('Contact', related_name='to_contacts')

#     class Meta:
#         unique_together = ('from_contact', 'to_contact')
