from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Skill)

admin.site.register(Country)

# fields to display for Organization model in Django admin
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('org_name','org_website')
admin.site.register(Organization, OrganizationAdmin)

# fields to display for City model in Django admin
class CityAdmin(admin.ModelAdmin):
    list_display = ('country','city')
admin.site.register(City, CityAdmin)

# fields to display for Posting model in Django admin
class PostingAdmin(admin.ModelAdmin):
    list_display = ('organization','title','city','last_updated_on','posting_url','contact_details')
admin.site.register(Posting, PostingAdmin)
