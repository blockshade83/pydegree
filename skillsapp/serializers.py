from rest_framework import serializers
from .models import *

# serializer for organization instances
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['user','org_name','about_org','org_website']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['skill_name']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city','country']

class PostingSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField('get_country')
    city = serializers.SerializerMethodField('get_city')
    org_name = serializers.SerializerMethodField('get_org_name')

    def get_org_name(self, obj):
        return obj.organization.org_name
        #return OrganizationSerializer(Organization.objects.get(id=obj.organization.id)).data['org_name']
    def get_city(self, obj):
        return obj.city.city
    def get_country(self, obj):
        return obj.city.country

    class Meta:
        model = Posting
        fields = ['org_name','title','last_updated_on','city','country']
