from django import forms
from skillsapp.models import Skill, Organization, Posting, PostingSkills
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.conf import settings

class OrganizationForm(UserCreationForm):
    email = forms.EmailField(required = True, label = 'Email')
    password1 = forms.CharField(required = True, label = 'password1')
    password2 = forms.CharField(required = True, label = 'password2')
    org_name = forms.CharField(required = True, label = 'Organization Name', max_length = 100)
    about_org = forms.CharField(required = True, label = 'About Organization', widget=forms.Textarea(attrs={'name':'body', 'rows':3, 'cols':50}))
    org_website = forms.CharField(required = True, label = 'Website', max_length = 100)
    logo = forms.FileField()

    # hide help text coming from UserCreationForm class settings
    # https://stackoverflow.com/questions/13202845/removing-help-text-from-django-usercreateform
    def __init__(self, *args, **kwargs):
        super(OrganizationForm, self).__init__(*args, **kwargs)

        for fieldname in ['email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ('email','org_name','about_org','org_website','logo')

class SkillCreateForm(forms.Form):
    skill_name = forms.CharField(required = True, label = 'Skill', max_length = 75)

    def clean(self):
        if self.cleaned_data.get('skill_name') == '':
            raise ValidationError('Field is mandatory')

# form for validating an update of organization details that also has a logo file
class OrgFormWithLogo(forms.Form):
    org_name = forms.CharField(required = True, label = 'Organization Name')
    about_org = forms.CharField(required = True, label = 'About Organization')
    org_website = forms.CharField(required = True, label = 'Website')
    logo = forms.FileField()

# form for validating an update of organization details that doesn't have a logo file
class OrgFormWithoutLogo(forms.Form):
    org_name = forms.CharField(required = True, label = 'Organization Name')
    about_org = forms.CharField(required = True, label = 'About Organization')
    org_website = forms.CharField(required = True, label = 'Website')

# form for validating a posting
class PostingForm(forms.Form):
    title = forms.CharField(required = True, label = 'Title')
    description = forms.CharField(required = True, label = 'Description')
    city = forms.ChoiceField(required = False, label = 'City')
    posting_url = forms.URLField(required = False, label = 'Posting URL')
    contact_details = forms.CharField(required = False, label = 'Contact Details')
    skills = forms.MultipleChoiceField(required = False, label = 'Skills')
