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
        return render(request, 'index.html')
    else:
        template = loader.get_template('index.html')
        return HttpResponse(template.render())

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
        contact_details = request.POST['contact_details']
        posted_on = datetime.today()
        last_updated_on = datetime.today()
        organization = Organization.objects.get(user=request.user)

        posting = Posting.objects.create(organization=organization,
                                         title=title,
                                         description=description,
                                         posting_url=posting_url,
                                         contact_details=contact_details,
                                         posted_on=posted_on,
                                         last_updated_on=last_updated_on)
        posting.save()
        return HttpResponse('Posting created')
    return render(request, 'add_posting.html')

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
