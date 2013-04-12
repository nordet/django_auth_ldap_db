# -*- coding: utf-8 -*-
'''
Created on 23 mars 2013

@author: pascal
'''
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ZimbraServerClass import ZimbraServerClass

class LdapServerClass(models.Model):
  host = models.CharField(_(u"host of Zimbra server"),
                          max_length=80, blank=False, null=False)
  port = models.IntegerField(_(u"port of Zimbra server"),
                             blank=False, null=False, default=389)
  user = models.CharField(_(u"user for Zimbra server"),
                          max_length=80, blank=False, null=False)
  password = models.CharField(_(u"password for Zimbra server"),
                              max_length=20, blank=True, null=True)
  userdn = models.CharField(_(u"user dn for Zimbra server"),
                            max_length=100, blank=False, null=False)
  userSearch = models.CharField(_(u"user search dn for Zimbra server"),
                                max_length=100, blank=False, null=False)
  userSearchScope = models.IntegerField(_(u"user search scope for Zimbra server"),
                                          default=2, blank=False, null=False)
  userSearchFilterStr = models.CharField(_(u"user search filter string for Zimbra server"),
                                         max_length=30, default='(uid=%(user)s)',
                                         blank=False, null=False)
  zimbraServer = models.ForeignKey(ZimbraServerClass)

  def __unicode__(self):
    return self.host
  
  class Meta:
    app_label = 'django_auth_ldap_db'
