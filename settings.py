# -*- coding: utf-8 -*-
'''
Created on 27 mars 2013

@author: pascal
'''
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
from django.core.context_processors import request

AUTH_LDAP_SERVER_URI = "ldap://mail.nordet.org"
AUTH_LDAP_BIND_DN = "uid=zimbra,cn=admins,cn=zimbra"
AUTH_LDAP_BIND_PASSWORD = "KvgU47sWM"
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=people,dc=nordet,dc=org", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

# Template context processors
TEMPLATE_CONTEXT_PROCESSORS = (
                               'django.contrib.auth.context_processors.auth',
                               'django.core.context_processors.debug',
                               'django.core.context_processors.media',
                               'django.core.context_processors.static',
                               'django.core.context_processors.request',
                               'django.core.context_processors.i18n',
                               'django.core.context_processors.csrf',
                               'django_auth_ldap_db.context_processors.currentZimbraServer'
                               )
