
from django.contrib import admin
from .models import Submission

from script.main import analyze

from traceback import print_exc


def make_analysis(modeladmin, request, queryset):
    for submission in queryset:
        try:
            print('analisando: '+str(submission))
            analyze(submission)

            submission.processed = True

            print('salvando')
            submission.save()

            print('OK')
        except:
            print('Análise falhou')

            print_exc()


class SubmissionAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'

    list_display = ('author', 'course', 'processed', 'last', 'timestamp')

    actions = [make_analysis]


admin.site.register(Submission, SubmissionAdmin)