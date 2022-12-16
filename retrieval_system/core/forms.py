from django import forms


class BooleanQueryForm(forms.Form):

    query = forms.CharField()
