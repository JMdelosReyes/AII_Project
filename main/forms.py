from django import forms
from main.models import Type


class ElementalTypeForm(forms.Form):
    type = forms.ChoiceField(choices=((t.name, t.name) for t in Type.objects.all()),
        widget = forms.Select(
            attrs = {'class': 'custom-select mr-sm-2', 'name': 'subject'}
        ))
