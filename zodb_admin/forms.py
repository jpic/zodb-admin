from django import forms

from models import Form


class FormCreateForm(forms.Form):
    name = forms.CharField()
    base = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super(FormCreateForm, self).__init__(*args, **kwargs)
        self.fields['base'].choices = [(n, n) for n, f in Form.db.items()]

    def save(self):
        return Form(self.cleaned_data['name']).save()


class ObjectCreateForm(forms.Form):
    catalog = forms.ChoiceField()
    name = forms.CharField()
    form = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(ObjectCreateForm, self).__init__(*args, **kwargs)
#        self.fields]'catalog'].choices = []
