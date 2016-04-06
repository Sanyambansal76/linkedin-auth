# Linkedin-auth
Linkedin-auth is an easy to setup linkedin authentication/registration mechanism with support for the Django Framework



Quick start
-----------

1. Installation:

    `pip install git+https://github.com/technoarch-softwares/linkedin-auth`

2. Add `"linkedin_login"` to your `INSTALLED_APPS` setting like this::

    INSTALLED_APPS = (
    
        ...
    
        'linkedin_login',
    
    )
    

3.   Add this lines to your project settings file:   
    
    `SITE_URL = 'SITE DOMIAN' #like 'http://localhost:8000/'`
    
    `ERROR_REDIRECT_URL = 'SITE LOGIN URL'`

    `LINKEDIN_REDIRECT_URL = 'linkedin/authentication'`

4.  Add Linkedin Secret Keys and Client Id    
    
    `LINKEDIN_CLIENT_ID = 'LINKEDIN API KEY'`
    
    `LINKEDIN_CLIENT_SECRET = 'LINKEDIN API SECRET'`
    
5. Include the `linkedin_login` URLconf in your project urls.py like this::

    `url(r'^linkedin/', include('linkedin_login.urls')),`

6. Run `python manage.py migrate` to create the `linkedin_login` models.

7. It will create a table into database named by `linkedin_login_linkedinprofile`.

8. Visit http://127.0.0.1:8000/linkedin/ to participate in the linkedin authentication.

#Features

1. Access the LINKEDIN API, from Your website (Using OAuth)

2. Django User Registration (Convert LINKEDIN user data into a user model)

3. Store user data locally.

4. LINKEDIN FQL access

5. Automated reauthentication (For expired tokens)
