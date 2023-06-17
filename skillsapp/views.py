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
    if request.user.is_authenticated:
        org_instance = Organization.objects.get(user=request.user)
        postings_instances = Posting.objects.filter(organization=org_instance)
    else:
        postings_instances = Posting.objects.all()
    postings_list = PostingSerializer(postings_instances, many=True).data
    # for element in postings_list:
    #     print(element)
    return render(request, 'index.html', {'postings': postings_list})

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
        # print(request.POST)
        # print(request.POST.getlist('skills_select'))
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

        return HttpResponse('Posting created')
    else:
        skills_instances = Skill.objects.all()
        skills_serializer = SkillSerializer(skills_instances, many=True)
        skills_dict = skills_serializer.data
        skills_list = []
        for element in skills_dict:
            skills_list.append(element['skill_name'])
        cities_instances = City.objects.all()
        cities_serializer = CitySerializer(cities_instances, many=True)
        cities_dict = cities_serializer.data
        cities_list = []
        for element in cities_dict:
            cities_list.append(element['city'])
        return render(request, 'add_posting.html', {'skills': skills_list, 'cities': cities_list})

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









































    #
