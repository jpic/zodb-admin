import urllib

from django import http
from django.utils import simplejson
from django.views import generic
from django.utils.translation import ugettext_lazy as _

from models import Form, Field
from forms import FormCreateForm, ObjectCreateForm


class FormCreateView(generic.FormView):
    template_name = 'zodb_admin/form/create.html'
    form_class = FormCreateForm

    def form_valid(self, form):
        query = '?base=' + urllib.quote(form.cleaned_data['base'])
        form = form.save()
        return http.HttpResponseRedirect(form.get_update_url() + query)


class FormUpdateView(generic.TemplateView):
    template_name = 'zodb_admin/form/update.html'

    def get_context_data(self, *args, **kwargs):
        base_form = self.request.GET.get('base', None)
        if base_form:
            base_form = Form.db.get(base_form, None)

        return {
            'KIND_CHOICES': Field.KIND_CHOICES,
            'form': Form.db[kwargs['name']],
            'base_form': base_form,
        }

    def post(self, *args, **kwargs):
        form_dict = simplejson.loads(self.request.POST['form'])
        form = Form.db[kwargs['name']]
        form.update_from_dict(form_dict)
        form.save()

        return http.HttpResponse(_(u'Form updated with success'))


class ObjectCreateView(generic.FormView):
    template_name = 'zodb_admin/object/form.html'
    form_class = ObjectCreateForm

    def form_valid(self, form):
        obj = Object(form.cleaned_data['catalog'], form.cleaned_data['name']
            ).save()

        form = form.save()

        return http.HttpResponseRedirect(form.get_update_url() + query)


class ObjectUpdateView(generic.TemplateView):
    template_name = 'zodb_admin/object/form.html'
