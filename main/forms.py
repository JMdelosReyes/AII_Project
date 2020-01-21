from django import forms
from main.models import Type, Generation


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


def get_generations():
    tup = ()
    tup = tup + (('-', '-'),)
    for g in Generation.objects.all():
        tup = tup + ((g.gen_id, g.gen_id),)
    return tup

class SearchForm(forms.Form):
    primary_type = forms.ChoiceField(choices=get_types_choices,
        widget = forms.Select(
            attrs = {'class': 'custom-select mr-sm-2'}
        ))
    secondary_type = forms.ChoiceField(choices=get_types_choices,
        widget = forms.Select(
            attrs = {'class': 'custom-select mr-sm-2'}
        ))
    generation = forms.ChoiceField(choices=get_generations,
        widget = forms.Select(
            attrs = {'class': 'custom-select mr-sm-2'}
        ))
    min_weight = forms.IntegerField(widget = forms.TextInput(
            attrs = {'class': 'form-control mr-sm-2'}
        ), initial=0)


