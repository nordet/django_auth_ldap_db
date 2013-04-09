# -*- coding: utf-8 -*-
'''
Created on 30 mars 2013

@author: pascal
'''
from django_auth_ldap_db.models.ZimbraServerClass import ZimbraServerClass
from django_auth_ldap_db.models.LdapServerClass import LdapServerClass
from rope.base.builtins import Str

try:
    set
except NameError:
    from sets import Set as set  # Python 2.3 fallback

import sys
import traceback
import pprint
import copy

import django.db
from django.contrib.auth.models import User, Group, Permission, SiteProfileNotAvailable
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
import django.dispatch
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import authenticate, login, logout

# Support Django 1.5's custom user models
try:
    from django.contrib.auth import get_user_model
    get_user_username = lambda u: u.get_username()
except ImportError:
    get_user_model = lambda: User
    get_user_username = lambda u: u.username


from django_auth_ldap.config import _LDAPConfig, LDAPSearch
from django_auth_ldap.backend import LDAPBackend

logger = _LDAPConfig.get_logger()


class LDAPBackendDB(LDAPBackend):
  
  def __init__(self):
    # LDAPBackend.__init__()
    print "===== LDAPBackendDB.__init__"
    # print "===== _get_settings : ", self._get_settings()
    self.__zimbraServer = None
    # self._get_settings()
    # print "===== LDAPBackendDB.__init__ : zimbraServer", self.__zimbraServer
    
  def _get_settings(self):
    print "===== LDAPBackendDB._get_settings : self._settings = ", self._settings
    if self._settings is None:
      print "===== LDAPBackendDB._get_settings : self.__zimbraServer = ", self._get_zimbraServer()
      self._settings = LDAPSettingsDB(self.settings_prefix, self.__zimbraServer)
    return self._settings
  
  def _set_zimbraServer(self, zimbraServer=None):
    self.__zimbraServer = zimbraServer
    print "===== _set_zimbraServer : self.__zimbraServer = ", self.__zimbraServer
  
  def _get_zimbraServer(self):
    return self.__zimbraServer
  
      #
    # The Django auth backend API
    #

    # def authenticate(self, username, password):
      # print "===== authenticate(self, username, password, LDAPServer = None):"



class LDAPSettingsDB(object):
  """
  This is a simple class to take the place of the global settings object. An
  instance will contain all of our settings as attributes, with default values
  if they are not specified by the configuration.
  """
  defaults = {
              'ALWAYS_UPDATE_USER': True,
              'AUTHORIZE_ALL_USERS': False,
              'BIND_AS_AUTHENTICATING_USER': False,
              'BIND_DN': '',
              'BIND_PASSWORD': '',
              'CACHE_GROUPS': False,
              'CONNECTION_OPTIONS': {},
              'DENY_GROUP': None,
              'FIND_GROUP_PERMS': False,
              'GROUP_CACHE_TIMEOUT': None,
              'GROUP_SEARCH': None,
              'GROUP_TYPE': None,
              'MIRROR_GROUPS': False,
              'PERMIT_EMPTY_PASSWORD': False,
              'PROFILE_ATTR_MAP': {},
              'PROFILE_FLAGS_BY_GROUP': {},
              'REQUIRE_GROUP': None,
              'SERVER_URI': 'ldap://localhost',
              'START_TLS': False,
              'USER_ATTR_MAP': {},
              'USER_DN_TEMPLATE': None,
              'USER_FLAGS_BY_GROUP': {},
              'USER_SEARCH': None,
  }

  def __init__(self, prefix='AUTH_LDAP_', zimbraServer=None):
    """
    Loads our settings from django.conf.settings, applying defaults for any
    that are omitted.
    """
    print "===== LDAPSettingsDB.__init__ : zimbraServer = ", zimbraServer
    print "===== LDAPSettingsDB.__init__ : defaults = ", self.defaults
    # print "===== LDAPSettingsDB.__init__ : currentZimbraServer = ", currentZimbraServer
    from django.conf import settings
    if zimbraServer is not None:
      zimbraServerDb = ZimbraServerClass.objects.get(host=zimbraServer)
      print "===== LDAPSettingsDB.__init__ : zimbraServerDb = ", zimbraServerDb
      ldap_db = LdapServerClass.objects.get(zimbraServer_id=zimbraServerDb.id)
      print "===== LDAPSettingsDB.__init__ : ldap_dp = ", ldap_db
      setattr(self, 'SERVER_URI', 'ldap://' + str(ldap_db.host) + ':' + str(ldap_db.port))
      setattr(self, 'BIND_DN', str(ldap_db.userdn))
      setattr(self, 'BIND_PASSWORD', str(ldap_db.password))
      LDAPSearch_db = LDAPSearch(str(ldap_db.userSearch), ldap_db.userSearchScope, ldap_db.userSearchFilterStr)
      # chaine = 'LDAPSearch("' + str(ldap_db.userSearch) + '", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")'
      # print "===== LDAPSettingsDB.__init__ : chaine USER_SEARCH = ", chaine
      setattr(self, 'USER_SEARCH', LDAPSearch_db)
    for name, default in self.defaults.iteritems():
      if (zimbraServer is None) or ((name != 'SERVER_URI') and
                                     (name != 'BIND_DN') and
                                     (name != 'BIND_PASSWORD') and
                                     (name != 'USER_SEARCH')):
        value = getattr(settings, prefix + name, default)
        if name == 'USER_SEARCH':
          print "===== LDAPSettingsDB.__init__ : name ", name
          print "===== LDAPSettingsDB.__init__ : default ", default
          print "===== LDAPSettingsDB.__init__ : value.base_dn = ", value.base_dn
          print "===== LDAPSettingsDB.__init__ : value.scope = ", value.scope
          print "===== LDAPSettingsDB.__init__ : value.filterstr = ", value.filterstr
          print "===== LDAPSettingsDB.__init__ : value.ldap = ", value.ldap
        else:
          print "===== LDAPSettingsDB.__init__ : name ", name
          print "===== LDAPSettingsDB.__init__ : default ", default
          print "===== LDAPSettingsDB.__init__ : value = ", value
        setattr(self, name, value)
