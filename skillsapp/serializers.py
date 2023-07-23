from rest_framework import serializers
from .models import *

# serializer for organization instances
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['user','org_name','about_org','org_website','logo']

# serializer for skill instances
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['skill_name']

# serializer for city instances
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city','country']

# serializer for skills related to a posting
class PostingSkillsSerializer(serializers.ModelSerializer):
    skill_name = serializers.SerializerMethodField('get_skill_name')

    #get skill names
    def get_skill_name(self, obj):
        return obj.skill.skill_name
    class Meta:
        model = PostingSkills
        fields = ['skill_name']

# serializer for posting instances
class PostingSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField('get_country')
    city = serializers.SerializerMethodField('get_city')
    org_name = serializers.SerializerMethodField('get_org_name')
    about_org = serializers.SerializerMethodField('get_about_org')
    logo = serializers.SerializerMethodField('get_org_logo')
    skills = serializers.SerializerMethodField('get_skills')

    # get org name from Organization model
    def get_org_name(self, obj):
        return obj.organization.org_name
    # get about org from Organization model
    def get_about_org(self, obj):
        return obj.organization.about_org
    # get logo from Organization model
    def get_org_logo(self, obj):
        try:
            if obj.organization.logo.url:
                return obj.organization.logo.url
        except:
            return None
    # get city name from City model
    def get_city(self, obj):
        return obj.city.city
    # get country name from City/Country models
    def get_country(self, obj):
        return obj.city.country
    # get skills for posting
    def get_skills(self, obj):
        posting_skill_instances = PostingSkills.objects.filter(posting=obj)
        return PostingSkillsSerializer(posting_skill_instances, many=True).data

    class Meta:
        model = Posting
        fields = ['id','org_name','about_org','logo','title','last_updated_on','deactivated','city','country','description','contact_details','posting_url','skills']
