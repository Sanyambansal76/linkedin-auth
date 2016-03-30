from django.db import models
from django.contrib.auth.models import User


class LinkedinProfile(models.Model):
    user = models.ForeignKey(User)
    linkedin_id = models.CharField(max_length=1000)
    access_token = models.CharField(max_length=1000)
    profile_data = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.user.first_name
