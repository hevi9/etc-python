from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from web.browser.views import file1
import web.webtest.views
import web.stats.views

urlpatterns = patterns('',
    # Example:
    # (r'^web/', include('web.foo.urls')),
    ('^stats/(.*)$', web.stats.views.stats),

    ('^file/(.*)$', file1),
    ('^file1/(.*)$', web.webtest.views.file1),



    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
)
