from django import forms
from degree.models import Grid
from datetime import datetime


class GridForm(forms.ModelForm):
    disciplinas = forms.FileField()
    prerequisitos = forms.FileField()
    equivalencias = forms.FileField()
    version = forms.IntegerField(initial=datetime.now().year)

    class Meta:
        model = Grid
        fields = [
            'disciplinas',
            'prerequisitos',
            'equivalencias',
            'version'
                ]
