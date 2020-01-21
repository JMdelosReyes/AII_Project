from django import forms
from main.models import Type


class ElementalTypeForm(forms.Form):
    type = forms.ChoiceField(choices=((t.name, t.name) for t in Type.objects.all()),
        widget = forms.Select(
            attrs = {'class': 'custom-select mr-sm-2', 'name': 'subject'}
        ))



def get_types_choices():
    tup = ()
    tup = tup + (('-', '-'),)
    for t in Type.objects.all():
        tup = tup + ((t.name, t.name),)
    return tup


class SearchForm(forms.Form):
#     name = forms.CharField(label='Name', max_length=30, widget = forms.TextInput(
#             attrs = {'class': 'form-control'}
#         ))
    primary_type = forms.ChoiceField(choices=get_types_choices,
        widget = forms.Select(
            attrs = {'class': 'custom-select mr-sm-2'}
        ))
    secondary_type = forms.ChoiceField(choices=get_types_choices,
        widget = forms.Select(
            attrs = {'class': 'custom-select mr-sm-2'}
        ))


