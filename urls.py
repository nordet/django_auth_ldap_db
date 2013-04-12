# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django_auth_ldap_db import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'home', name='home'),
    # url(r'^testConnexionLdapDjango/', include('testConnexionLdapDjango.foo.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^login', 'django_auth_ldap_db.views.login_interne', name='login_interne'),
    url(r'^login_interne', 'django_auth_ldap_db.views.login_interne', name='login_interne'),
    url(r'^logout_view$', 'django_auth_ldap_db.views.logout_view', name='logout_view'),
)
