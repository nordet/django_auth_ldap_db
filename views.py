# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django_auth_ldap_db.forms.LoginForm import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django_auth_ldap_db.backend import LDAPBackendDB


def login_interne(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['userName']
      password = form.cleaned_data['userPassword']
      zimbraServer = form.cleaned_data['host']
      request.session['currentZimbraServer'] = zimbraServer
      # request.session.modified = True
      print "===== login_interne : zimbraServer = ", zimbraServer
      # user = authenticate(username=username, password=password)
      backend = LDAPBackendDB()
      backend._set_zimbraServer(zimbraServer)
      backend._get_settings()
      # user = authenticate(username=username, password=password)
      # print "===== login_interne : type(user) = ", type(user)
      # print "===== login_interne : user = ", user
      user = backend.authenticate(username=username, password=password)
      if user is not None:
        user.backend = 'django_auth_ldap_db.backend.LDAPBackendDB'
        if user.is_active:
          login(request, user)
          request.session['currentZimbraServer'] = zimbraServer
          return render_to_response('home.html', context_instance=RequestContext(request))
        else:
          # return HttpResponse("Compte inexistant !")
          logout(request)
          messageType = "warning"
          message = "Compte inexistant !"
          return render_to_response('message.html', {'STATIC_URL': settings.STATIC_URL,
                                                     'messageType': messageType, 'message': message},
                                    context_instance=RequestContext(request))
      else:
        logout(request)
        messageType = "warning"
        message = "Compte inexistant !"
        return render_to_response('message.html', {'STATIC_URL': settings.STATIC_URL,
                                                   'messageType': messageType, 'message': message},
                                  context_instance=RequestContext(request))
    else:
      # return HttpResponse("Identifiant ou mot de passe incorrect !")
      logout(request)
      messageType = "warning"
      message = "Identifiant ou mot de passe incorrect !"
      return render_to_response('message.html', {'STATIC_URL': settings.STATIC_URL,
                                                 'messageType': messageType, 'message': message},
                                context_instance=RequestContext(request))
  else:
    form = LoginForm()
    return render_to_response('login.html',
                              {'form': form, },
                              context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def home(request):
  return render_to_response('home.html', context_instance=RequestContext(request))

def message(request, messageType, message):
    return render_to_response('message.html', context_instance=RequestContext(request))

