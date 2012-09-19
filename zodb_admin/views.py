import urllib
import copy

from django import http
from django.utils import simplejson
from django.views import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.urlresolvers import reverse

import transaction

from forms import FormCreateForm, CatalogCreateForm
from models import Catalog, Form, Field, get_object_map


class CatalogCreateView(generic.FormView):
    form_class = CatalogCreateForm
    template_name = 'zodb_admin/base_form.html'

    def form_valid(self, form):
        catalog = form.save()
        Catalog.db[catalog.name] = catalog
        transaction.commit()
        return http.HttpResponseRedirect(reverse('zodb_admin:form_create')
                + '?' + urllib.urlencode({'catalog': catalog.name}))


class FormCreateView(generic.FormView):
    form_class = FormCreateForm
    template_name = 'zodb_admin/base_form.html'

    def get_initial(self):
        return {'catalog': self.request.GET.get('catalog')}

    def form_valid(self, form):
        form = form.save()
        Form.db[form.name] = form
        transaction.commit()
        return http.HttpResponseRedirect(form.get_update_url())


class FormUpdateView(generic.TemplateView):
    template_name = 'zodb_admin/form/update.html'

    def get_context_data(self, *args, **kwargs):
        return {
            'KIND_CHOICES': Field.KIND_CHOICES,
            'form': Form.db[kwargs['name']],
        }

    def post(self, *args, **kwargs):
        form_dict = simplejson.loads(self.request.POST['form'])
        form = Form.db[kwargs['name']]
        form.update_from_dict(form_dict)
        transaction.commit()

        return http.HttpResponse(_(u'Form updated with success'))


class RecordUpdateView(generic.TemplateView):
    template_name = 'zodb_admin/object/update.html'
