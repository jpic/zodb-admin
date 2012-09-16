from django.conf.urls import patterns, url

from views import (FormCreateView, FormUpdateView, ObjectCreateView,
        ObjectUpdateView)

urlpatterns = patterns('zodb_admin.views',
    url('form/create/$', FormCreateView.as_view(), name='form_create'),
    url('form/update/(?P<name>.+)/$', FormUpdateView.as_view(),
        name='form_update'),
    url('object/create/$', ObjectCreateView.as_view(), name='object_create'),
    url('object/(?P<name>.+)/update/(?P<base_name>)/$',
        ObjectUpdateView.as_view(), name='object_update'),
)
