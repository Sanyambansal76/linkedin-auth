import requests
import urllib2
import urllib
import json
import ast

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, get_backends, logout
from django.contrib.auth.decorators import login_required

from linkedin_login.models import LinkedinProfile
from linkedin_login.utils import create_username
from linkedin_login.forms import EmailForm


linkedin_redirect_url = settings.SITE_URL + settings.LINKEDIN_REDIRECT_URL


def linkedin_login(request):
    """
        To send the request to linkedin API for the authorization code by the use of client id.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect('%s%s' % (settings.SITE_URL, settings.LOGIN_REDIRECT_URL))

    url = 'https://www.linkedin.com/uas/oauth2/authorization?response_type=code&client_id=%s&redirect_uri=%s&state=987654321&scope=r_basicprofile r_emailaddress' \
        % (settings.LINKEDIN_CLIENT_ID, linkedin_redirect_url)

    return HttpResponseRedirect(url)


def get_linkedin_access_token(code):
    """
        Code is used to get the access token by use of client id and client secret.
    """
    access_token_url = 'https://www.linkedin.com/uas/oauth2/accessToken'

    post_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': linkedin_redirect_url,
        'client_id': settings.LINKEDIN_CLIENT_ID,
        'client_secret': settings.LINKEDIN_CLIENT_SECRET,
    }

    headers ={
        'Host': 'www.linkedin.com',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(access_token_url, data=post_data, headers=headers)

    response_dict = ast.literal_eval(response.text)

    access_token = response_dict['access_token']

    return access_token


def get_linkedin_user_info(access_token):
    """
        Access token is use for getting the linkedin user info and email address.
    """
    query_string = {'oauth2_access_token': access_token, 'format': 'json'}

    profile_url = 'https://api.linkedin.com/v1/people/~'
    profile_response = requests.get(profile_url, params=query_string)
    profile_response_dict = ast.literal_eval(profile_response.text)
    profile_response_json = json.dumps(profile_response.text)

    email_url = 'https://api.linkedin.com/v1/people/~/email-address'
    email_response = requests.get(email_url, params=query_string)
    email_response_str = ast.literal_eval(email_response.text)

    return (profile_response_json, profile_response_dict, email_response_str)


def linkedin_authentication(request):
    """
        It is the main function and view for the linkedin redirect uri for calling the other functions.
    """
    try:
        code = request.GET['code']
    except:
        messages.error(request, "Sorry we can't log you in. Please try again.")
        return HttpResponseRedirect(settings.ERROR_REDIRECT_URL)

    try:
        access_token = get_linkedin_access_token(code)
    except:
        return HttpResponseRedirect(settings.ERROR_REDIRECT_URL)

    try:
        profile_response_json, profile_response_dict, email_response_str = get_linkedin_user_info(access_token)
    except:
        return HttpResponseRedirect(settings.ERROR_REDIRECT_URL)

    member_id = profile_response_dict['id']

    try:
        linkedin_profile = LinkedinProfile.objects.get(linkedin_id=member_id)
        user = linkedin_profile.user

        if access_token != linkedin_profile.access_token:
            linkedin_profile.access_token = access_token
            linkedin_profile.save()

        linkedin_profile.profile_data = profile_response_json
        linkedin_profile.save()

    except LinkedinProfile.DoesNotExist:
        email_response_str = ''
        if email_response_str != '':
            try:
                user = User.objects.get(email__iexact=email_response_str)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    email=email_response_str,
                    username=create_username(profile_response_dict['firstName'].title() + ' ' + profile_response_dict['lastName'].title()),
                    first_name = profile_response_dict['firstName'].title(),
                    last_name = profile_response_dict['lastName'].title(),
                )

            LinkedinProfile.objects.create(
                user=user,
                linkedin_id=member_id,
                access_token=access_token,
                profile_data=profile_response_json,
            )
        else:
            request.session['access_token'] = access_token
            request.session['profile_response_dict'] = profile_response_dict
            request.session['profile_response_json'] = profile_response_json

            return HttpResponseRedirect(reverse('email_form'))

    user.backend = "django.contrib.auth.backends.ModelBackend"
    login(request, user)

    return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)


def linkedin_email_form(request):
    form = EmailForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            try:
                user = User.objects.get(email__iexact=form.cleaned_data['email'])
            except User.DoesNotExist:
                user = User.objects.create_user(
                    email=form.cleaned_data['email'],
                    username=create_username(request.session['profile_response_dict']['firstName'].title() + ' ' + request.session['profile_response_dict']['lastName'].title()),
                    first_name = request.session['profile_response_dict']['firstName'].title(),
                    last_name = request.session['profile_response_dict']['lastName'].title(),
                )

            LinkedinProfile.objects.create(
                user=user,
                linkedin_id=request.session['profile_response_dict']['id'],
                access_token=request.session['access_token'],
                profile_data=request.session['profile_response_json'],
            )

            user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, user)

            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    return render_to_response('linkedin_email_form.html', {
        'form': form
    }, context_instance=RequestContext(request))
