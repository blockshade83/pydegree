from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants as messages
from datetime import datetime
from .forms import *
from .serializers import *

def index(request):
    posting_instances = Posting.objects.all()
    # initialize city, org, skill objects
    city = None
    org = None
    skill = None

    if request.method == 'POST':
        # check if a value was passed for city via filtering
        try:
            city = request.POST['city_select']
        except:
            pass

        # check if a value was passed for organization via filtering
        try:
            org = request.POST['org_select']
        except:
            pass

        # check if a value was passed for a skill via filtering
        try:
            skill = request.POST['skill_select']
        except:
            pass

        # filter instances by city if a city was used as a filter
        if city:
            city_instance = City.objects.get(city=city)
            posting_instances = posting_instances.filter(city=city_instance)
        # filter instances by organization if an organization was used as a filter
        if org:
            org_instance = Organization.objects.get(org_name=org)
            posting_instances = posting_instances.filter(organization=org_instance)
        # filter instances by skill if a skills was used as a filter
        if skill:
            skill_instance = Skill.objects.get(skill_name=skill)
            posting_skills_instances = PostingSkills.objects.filter(skill=skill_instance)
            posting_id_list = []
            for instance in posting_skills_instances:
                posting_id_list.append(instance.posting.id)
            posting_instances = posting_instances.filter(id__in=posting_id_list)

    # filter instances by keyword if the keyword is found in the description
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        if keyword:
            posting_instances = posting_instances.filter(description__icontains=keyword)

    # serialize data for postings
    postings_list = PostingSerializer(posting_instances, many=True).data
    # get list of all cities in the database to populate dropdown list
    cities_list = get_cities_list()
    # get list of all organizations in the database to populate dropdown list
    org_list = get_org_list()
    # get list of all skills in the database to populate dropdown list
    skills_list = get_skills_list()
    return render(request, 'index.html', {'postings': postings_list,
                                          'cities': cities_list,
                                          'organizations': org_list,
                                          'skills': skills_list,
                                          'city_selection': city,
                                          'org_selection': org,
                                          'skill_selection': skill })

def register(request):
    if request.method == 'POST':
        username = request.POST['email']
        org_name = request.POST['org_name']
        about_org = request.POST['about_org']
        org_website = request.POST['org_website']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return HttpResponseRedirect('register')

        user = User.objects.create_user(username=username, password=password1)
        organization = Organization.objects.create(user=user,
                                                   org_name=org_name,
                                                   about_org=about_org,
                                                   org_website=org_website)
        user.save()
        organization.save()
        return HttpResponse('Account was created')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # attempt authentication
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            # error when attempting to authenticate
            return render(request, 'login.html', {'error': True})
    else:
        # request method is not POST
        return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def add_posting(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        posting_url = request.POST['posting_url']
        contact_details = request.POST.getlist('contact_details')
        posted_on = datetime.today()
        last_updated_on = datetime.today()
        skills = request.POST.getlist('skills_select')
        city = request.POST['city_select']
        organization = Organization.objects.get(user=request.user)

        if (posting_url == "" and contact_details == ""):
            return HttpResponse('Posting URL can be blank only if alternative contact details are specified')

        posting = Posting.objects.create(organization=organization,
                                         title=title,
                                         description=description,
                                         city=City.objects.get(city=city),
                                         posting_url=posting_url,
                                         contact_details=contact_details,
                                         posted_on=posted_on,
                                         last_updated_on=last_updated_on)
        posting.save()

        for skill in skills:
            skill_instance = Skill.objects.get(skill_name=skill)
            posting_skill = PostingSkills.objects.create(skill=skill_instance,posting=posting)
            posting_skill.save()

    else:
        # get list of skills in the database to populate selection forms
        skills_list = get_skills_list()
        # get list of cities in the database to populate selection forms
        cities_list = get_cities_list()
        return render(request, 'add_posting.html', {'skills': skills_list, 'cities': cities_list})

def view_posting(request, posting_id):
    if request.method == 'GET':
        posting_instance = Posting.objects.get(id=posting_id)
        posting = PostingSerializer(posting_instance).data
        return render(request, 'view_posting.html', {'posting': posting})
    else:
        return HttpResponseRedirect('/')

@login_required
def my_postings(request):
    if request.method == 'GET':
        org_instance = Organization.objects.get(user=request.user)
        posting_instances = Posting.objects.filter(organization=org_instance)
        postings_list = PostingSerializer(posting_instances, many=True).data
        return render(request, 'my_postings.html', {'postings': postings_list})
    else:
        return HttpResponseRedirect('/')

@login_required
def edit_posting(request, posting_id):
    if request.method == 'POST':
        if (request.POST['posting_url'] == "" and request.POST['description'] == ""):
            return HttpResponse('Posting URL can be blank only if alternative contact details are specified')
        try:
            # get posting instance based on id
            posting_instance = Posting.objects.get(id=posting_id)

            # set new values for posting attributes
            posting_instance.title = request.POST['title']
            posting_instance.description = request.POST['description']
            posting_instance.posting_url = request.POST['posting_url']
            posting_instance.contact_details = request.POST.getlist('contact_details')
            posting_instance.last_updated_on = datetime.today()
            posting_instance.city = City.objects.get(city=request.POST['city_select'])

            # get list of skills submitted via the edit form
            skills = request.POST.getlist('skills_select')

            # get all instances of posting skills previously saved for the selected posting
            posting_skill_instances = PostingSkills.objects.filter(posting=posting_instance)
            # iterate over all posting skills for the selected posting
            for instance in posting_skill_instances:
                # if the existing skill for the posting is no longer a part of the updated list, delete the instance
                if instance.skill.skill_name not in skills:
                    instance.delete()

            # iterate over the updated list of skills submitted with the edit form
            for skill in skills:
                # get instance for the skill based on the name
                skill_instance = Skill.objects.get(skill_name=skill)
                # create instance if it doesn't exist
                posting_skill_instance = PostingSkills.objects.get_or_create(posting=posting_instance,skill=skill_instance)

            posting_instance.save()

            return HttpResponse('Posting updated')
        except Posting.DoesNotExist:
            return HttpResponseRedirect('/')
    else:
        # get posting instance
        posting_instance = Posting.objects.get(id=posting_id)
        posting = PostingSerializer(posting_instance).data
        # get list of skills in the database to populate selection forms
        skills_list = get_skills_list()
        # get list of cities in the database to populate selection forms
        cities_list = get_cities_list()
        # define dictionary to match selected skills for posting in the list of all skills
        # this will support pre-populating the selected skills in the dropdown list
        skills_intersected = {}
        # iterate over all existing skills
        for skill in skills_list:
            # define skill as being not selected in the posting to start with
            skills_intersected[skill] = 'no'
            # iterate over the skills selected for the specific job posting
            for posting_skill in posting['skills']:
                # set value in dictionary as yes if the skill is also found in the posting
                if skill == posting_skill['skill_name']:
                    skills_intersected[skill] = 'yes'
        return render(request, 'edit_posting.html', {'posting': posting, 'skills': skills_intersected, 'cities': cities_list})

@login_required
def reconfirm_posting(request, posting_id):
    if request.method == 'GET':
        try:
            # get posting instance based on id
            posting_instance = Posting.objects.get(id=posting_id)
            posting_instance.last_updated_on = datetime.today()
            posting_instance.save()
        except Posting.DoesNotExist:
            return HttpResponseRedirect('/')
    return HttpResponseRedirect('/my_postings')

@login_required
def update_org_details(request):
    organization = Organization.objects.get(user=request.user)
    if request.method == 'POST':
        org_name = request.POST['org_name']
        about_org = request.POST['about_org']
        org_website = request.POST['org_website']

        organization.org_name = org_name
        organization.about_org = about_org
        organization.org_website = org_website

        organization.save()
        return HttpResponseRedirect('/')

    else:
        return render(request, 'update_org_details.html', {'organization': organization})

# get list of cities in the database to populate selection forms
def get_cities_list():
    cities_instances = City.objects.all()
    cities_serializer = CitySerializer(cities_instances, many=True)
    cities_dict = cities_serializer.data
    cities_list = []
    for element in cities_dict:
        cities_list.append(element['city'])
    return cities_list

# get list of organizations in the database to populate selection forms
def get_org_list():
    org_instances = Organization.objects.all()
    org_serializer = OrganizationSerializer(org_instances, many=True)
    org_dict = org_serializer.data
    org_list = []
    for element in org_dict:
        org_list.append(element['org_name'])
    return org_list

# get list of skills in the database to populate selection forms
def get_skills_list():
    skills_instances = Skill.objects.all()
    skills_serializer = SkillSerializer(skills_instances, many=True)
    skills_dict = skills_serializer.data
    skills_list = []
    for element in skills_dict:
        skills_list.append(element['skill_name'])
    return sorted(skills_list)






































    #
