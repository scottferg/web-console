from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm

admin.autodiscover()

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    (r'^$', 'console.views.index'),
    (r'^submit/$', 'console.views.submit'),

    (r'^admin/', include(admin.site.urls)),
)
