# Linkedin-auth
Linkedin-auth is an easy to setup linkedin authentication/registration mechanism with support for the Django Framework



Quick start
-----------

1. Move to project directory run command::

    `pip install git+https://github.com/technoarch-softwares/linkedin-auth`

2. Add `"linkedin_login"` to your `INSTALLED_APPS` setting like this::

    INSTALLED_APPS = (
    
        ...
    
        'linkedin_login',
    
    )
    
    `SITE_URL = 'SITE DOMIAN' #like 'http://localhost:8000/'`
    
    `ERROR_REDIRECT_URL = 'SITE LOGIN URL'`
    
    `LINKEDIN_CLIENT_ID = 'LINKEDIN API KEY'`
    
    `LINKEDIN_CLIENT_SECRET = 'LINKEDIN API SECRET'`
    
    `LINKEDIN_REDIRECT_URL = 'linkedin/authentication'`

3. Include the `linkedin_login` URLconf in your project urls.py like this::

    `url(r'^linkedin/', include('linkedin_login.urls')),`

4. Run `python manage.py migrate` to create the `linkedin_login` models.

5. It will create a table into database named by `linkedin_login_linkedinprofile`.

6. Visit http://127.0.0.1:8000/linkedin/ to participate in the linkedin authentication.

