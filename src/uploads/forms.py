from django import forms
from datetime import datetime
from uploads.models import Submission


class SubmissionForm(forms.ModelForm):
    historico = forms.FileField()
    matricula = forms.FileField()
    semester_status = forms.ChoiceField(choices=Submission.STATUS_CHOICES)
    relative_year = forms.IntegerField(initial=datetime.now().year)
    relative_semester = forms.IntegerField(initial=1)

    class Meta:
        model = Submission
        fields = [
                'historico',
                'matricula',
                'semester_status',
                'relative_year',
                'relative_semester',
                'degree'
                ]
