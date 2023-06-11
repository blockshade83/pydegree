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
