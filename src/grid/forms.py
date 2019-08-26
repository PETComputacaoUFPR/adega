from django import forms
from datetime import datetime
from grid.models import Grid


class GridForm(forms.ModelForm):
    disciplinas = forms.FileField()
    equivalencias = forms.FileField()
    version = forms.IntegerField(initial=datetime.now().year)

    class Meta:
        model = Grid
        fields = [
            'version',
            'disciplinas',
            'equivalencias',
            'degree'
                ]
