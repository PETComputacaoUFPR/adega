from django.contrib import admin
from submission.models import Submission

from submission.analysis.main import analyze

from traceback import print_exc


def make_analysis(modeladmin, request, queryset):
    for submission in queryset:
        try:
            print('analisando: '+str(submission))
            analyze(submission)

            print('OK')
        except:
            print('Análise falhou')

            print_exc()


class SubmissionAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'

    list_display = ('author', 'degree', 'processed', 'last', 'timestamp')

    actions = [make_analysis]


admin.site.register(Submission, SubmissionAdmin)
