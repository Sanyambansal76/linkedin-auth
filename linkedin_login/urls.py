from django.conf.urls import include, url


urlpatterns = [
    url(r'^$', 'linkedin_login.views.linkedin_login', name="linkedin_login"),
    url(r'^authentication/$', 'linkedin_login.views.linkedin_authentication', name="linkedin_authentication"),
    url(r'^email-form/$', 'linkedin_login.views.linkedin_email_form', name="linkedin_email_form"),
    ]
