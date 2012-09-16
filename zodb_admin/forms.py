import copy

from django.utils.translation import ugettext_lazy as _
from django import forms

from models import Form, Catalog


class FormCreateForm(forms.Form):
    name = forms.CharField()
    base = forms.ChoiceField(required=False)
    catalog = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(FormCreateForm, self).__init__(*args, **kwargs)
        self.fields['base'].choices = [(n, n) for n, f in Form.db.items()]
        self.fields['base'].choices.append((None, _(u'Empty')))
        self.fields['catalog'].choices = [(n, n) for n, f in
                Catalog.db.items()]

    def clean_catalog(self):
        catalog = self.cleaned_data['catalog']
        try:
            Catalog.db[catalog]
        except KeyError:
            Catalog.db[catalog] = Catalog(name=catalog).save()
        return catalog

    def save(self):
        base = self.cleaned_data['base']

        if base:
            form = copy.deepcopy(Form.db[base])
            form.name = u'%s %s' % (_(u'Copy of'), form.name)
            return form.save()
        else:
            return Form(self.cleaned_data['name'],
                    Catalog.db[self.cleaned_data['catalog']]).save()


class ObjectCreateForm(forms.Form):
    catalog = forms.ChoiceField()
    name = forms.CharField()
    form = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(ObjectCreateForm, self).__init__(*args, **kwargs)
#        self.fields]'catalog'].choices = []
