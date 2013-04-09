# -*- coding: utf-8 -*-
'''
Created on 26 mars 2013

@author: pascal
'''
from django import forms
from django_auth_ldap_db.models.ZimbraServerClass import ZimbraServerClass

class LoginForm(forms.Form):
  userName = forms.CharField()
  userPassword = forms.CharField(widget=forms.PasswordInput())
  host = forms.ModelChoiceField(ZimbraServerClass.objects.all())
