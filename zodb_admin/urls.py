from django.conf.urls import patterns, url

from views import (FormCreateView, FormUpdateView, RecordUpdateView,
        CatalogCreateView)

urlpatterns = patterns('zodb_admin.views',
    url('catalog/create/$', CatalogCreateView.as_view(),
        name='catalog_create'),
    url('form/create/$', FormCreateView.as_view(), name='form_create'),
    url('form/update/(?P<name>.+)/$', FormUpdateView.as_view(),
        name='form_update'),
    url('record/(?P<catalog>.+)/(?P<name>.+)/update/$',
        RecordUpdateView.as_view(), name='record_update'),
)
