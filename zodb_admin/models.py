from importlib import import_module

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from crispy_forms.layout import Layout, Fieldset

from zodb_light.models import Model, RelationDescriptor


class Form(Model):
    catalog = RelationDescriptor('self',
            'zodb_admin.models.Catalog', 'tree', True)

    def __init__(self, name=None, tabs=None, inlines=None):
        super(Form, self).__init__(name)

        if tabs is None:
            tabs = []
        if inlines is None:
            inlines = []

    def get_update_url(self):
        return reverse('zodb_admin:form_update', args=[self.name])

    def to_crispy(self):
        layout = Layout()
        for tab in self.tabs:
            layout.fields.append(tab.to_crispy())

        return layout

    @property
    def fields(self):
        for tab in self.tabs:
            for field in tab.fields:
                yield field

    def update_from_dict(self, data):
        self.name = data[u'name'].strip()

        self.tabs = []
        order = 0

        for tab_data in data[u'tabs']:
            tab = Tab(self, tab_data[u'name'].strip(), order)
            tab.update_from_dict(tab_data)
            self.tabs.append(tab)
            order += 1


class Tab(object):
    def __init__(self, form, name, order=None, fields=None):
        if order is None:
            order = 0
        if fields is None:
            fields = []

        self.form = form
        self.name = name
        self.order = order
        self.fields = fields

    def to_crispy(self):
        fieldset = Fieldset(self.name)
        for field in self.fields:
            fieldset.fields.append(field.to_crispy())
        return fieldset

    def update_from_dict(self, data):
        self.fields = []
        order = 0

        for field_data in data[u'fields']:
            self.fields.append(Field(self,
                field_data[u'name'].strip(),
                field_data[u'kind'].strip(),
                field_data[u'required'],
                order,
                field_data[u'verbose_name'].strip(),
                field_data[u'help_text'].strip()
            ))
            order += 1

    def __unicode__(self):
        return self.name


class Field(object):
    KIND_CHOICES = (
        ('django.forms.fields.CharField', _(u'one line text')),
        ('django.forms.fields.IntegerField', _(u'integer')),
        ('django.forms.fields.DecimalField', _(u'decimal number')),
        ('django.forms.fields.DateField', _(u'date')),
        ('django.forms.fields.TimeField', _(u'time')),
        ('django.forms.fields.DateTimeField', _(u'date and time')),
        ('django.forms.fields.EmailField', _(u'email')),
        ('django.forms.fields.URLField', _(u'url')),
        ('django.forms.fields.BooleanField', _(u'yes/no')),
        ('django.forms.fields.NullBooleanField', _(u'yes/no/unknown')),
        ('django.forms.fields.IPAddressField', _(u'IP address')),
        ('django.forms.fields.RegexField', _(u'regexp')),
        ('django.forms.fields.SlugField', _(u'slug')),
    )

    def __init__(self, tab, name, kind, required=False, order=None,
            verbose_name=None, help_text=None):
        self.tab = tab
        self.name = name
        self.kind = kind
        self.required = required
        self.order = order
        self.verbose_name = verbose_name
        self.help_text = help_text

    def formfield_class(self):
        bits = self.kind.split('.')
        module = bits[:-1]
        cls = bits[-1]
        module = import_module(module)
        return getattr(module, cls)

    def formfield_kwargs(self):
        return {
            'label': self.name,
            'required': self.required,
            'help_text': self.help_text,
        }

    def formfield_instance(self):
        return self.formfield_class()(**self.formfield_kwargs())

    def __unicode__(self):
        return self.name


class Catalog(Model):
    parent = RelationDescriptor('zodb_admin.models.Catalog',
            'self', 'tree', True)
    children = RelationDescriptor('self',
            'zodb_admin.models.Catalog', 'tree')
    forms = RelationDescriptor('self',
            'zodb_admin.models.Form', 'tree')


class Record(Model):
    def __init__(self, catalog, name, fields):
        self.catalog = catalog
        self.name = fields['name']
        self.fields = fields

    @classmethod
    def create_urls(self, user):
        urls = {}

#        for catalog in Catalog.db.values():
#            url = reverse('zodb_admin:record_create', args=(catalog.name,))
#            urls[url] = catalog

        return urls

    def get_update_url(self):
        return reverse('zodb_admin:record_update', args=(self.catalog.name,
            self.name))
