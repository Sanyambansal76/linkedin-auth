from django.contrib import admin

from linkedin_login.models import LinkedinProfile


class LinkedinProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'linkedin_id', 'access_token', 'profile_data')
    list_filter = ('user__first_name', 'user__last_name', 'user__email', 'linkedin_id')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'linkedin_id')


admin.site.register(LinkedinProfile, LinkedinProfileAdmin)
