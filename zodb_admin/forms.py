import copy
import transaction

from django.utils.translation import ugettext_lazy as _
from django import forms

from models import Form, Catalog


class CatalogCreateForm(forms.Form):
    parent = forms.ChoiceField(choices=[], required=False)
    name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(CatalogCreateForm, self).__init__(*args, **kwargs)

        if not len(Catalog.db.keys()):
            self.fields.pop('parent')
        else:
            self.fields['parent'].choices = [(u'', _(u'None'))]
            self.fields['parent'].choices += [(k, n) for k, n in Catalog.db.items()]

    def clean_name(self):
        name = self.cleaned_data['name']
        if name in Catalog.db.keys():
            raise forms.ValidationError(
                    _(u'A catalog with this name already exists'))
        return name

    def clean_parent(self):
        parent = self.cleaned_data['parent']
        if parent and not Catalog.exists(parent):
            raise forms.ValidationError(
                    _(u'This catalog does not exist'))
        return parent

    def save(self):
        catalog = Catalog(name=self.cleaned_data['name'])

        parent = self.cleaned_data.get('parent', None)
        if parent:
            catalog.parent = Catalog.get(parent)

        return catalog


class FormCreateForm(forms.Form):
    catalog = forms.ChoiceField(choices=[])
    name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(FormCreateForm, self).__init__(*args, **kwargs)
        self.fields['catalog'].choices += [(k, n) for k, n in Catalog.db.items()]

    def clean_catalog(self):
        catalog = self.cleaned_data['catalog']
        if not Catalog.exists(catalog):
            raise forms.ValidationError(
                    _(u'This catalog does not exist'))
        return catalog

    def clean_name(self):
        name = self.cleaned_data['name']
        if name in Form.db.keys():
            raise forms.ValidationError(
                    _(u'There is already a form with this name'))
        return name

    def save(self):
        form = Form(name=self.cleaned_data['name'])
        form.catalog = Catalog.get(self.cleaned_data['catalog'])
        return form
