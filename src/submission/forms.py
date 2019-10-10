from django import forms
from datetime import datetime
from submission.models import Submission


class SubmissionForm(forms.ModelForm):
    csv_data_file = forms.FileField()
    semester_status = forms.ChoiceField(choices=Submission.STATUS_CHOICES)
    relative_year = forms.IntegerField(initial=datetime.now().year)
    relative_semester = forms.IntegerField(initial=1)

    class Meta:
        model = Submission
        fields = [
            'csv_data_file',
            'semester_status',
            'relative_year',
            'relative_semester',
            'degree'
            ]
