import copy
import transaction

from django.utils.translation import ugettext_lazy as _
from django import forms

from models import Form, Catalog, OBJECT_MAP


class CatalogCreateForm(forms.Form):
    parent = forms.ChoiceField(choices=[], required=False)
    name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(CatalogCreateForm, self).__init__(*args, **kwargs)

        if not len(Catalog.db.keys()):
            self.fields.pop('parent')
        else:
            self.fields['parent'].choices = [(u'', _(u'None'))]
            self.fields['parent'].choices += [(n, n) for n in Catalog.db.keys()]

    def clean_name(self):
        name = self.cleaned_data['name']
        if name in Catalog.db.keys():
            raise forms.ValidationError(
                    _(u'A catalog with this name already exists'))
        return name

    def clean_parent(self):
        parent = self.cleaned_data['parent']
        if parent and parent not in Catalog.db.keys():
            raise forms.ValidationError(
                    _(u'This catalog does not exist'))
        return parent

    def save(self):
        catalog = Catalog(name=self.cleaned_data['name'])
        OBJECT_MAP.add(catalog)

        parent = self.cleaned_data.get('parent', None)
        if parent:
            parent = Catalog.db[parent]

            OBJECT_MAP.connect(parent, catalog, 'children')

        Catalog.db[catalog.name] = catalog
        transaction.commit()
        return catalog


class FormCreateForm(forms.Form):
    catalog = forms.ChoiceField(choices=[])
    name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(FormCreateForm, self).__init__(*args, **kwargs)
        self.fields['catalog'].choices += [(n, n) for n in Catalog.db.keys()]

    def clean_catalog(self):
        catalog = self.cleaned_data['catalog']
        if catalog not in Catalog.db.keys():
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
        OBJECT_MAP.add(form)

        catalog = Catalog.db[self.cleaned_data['catalog']]

        OBJECT_MAP.connect(catalog, form, 'forms')

        Form.db[form.name] = form
        transaction.commit()

        return form
