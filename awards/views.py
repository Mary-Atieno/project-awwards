from django import views
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from .forms import *
from django.http import HttpResponseRedirect
from . models import *
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib import messages
from .serializer import *
from .decorators import *
from .permissions import IsAdminOrReadOnly

# from rest_framework import status


# Create your views here.
@login_required(login_url='/accounts/login/')
def p_rating(request, post):
    post = Project.objects.get(title=post)
    ratings = Ratings.objects.filter(user=request.user, post=post).first()
    rating_status = None
    if ratings is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.post = post
            rate.save()
            post_ratings = Ratings.objects.filter(post=post)

            design_ratings = [d.design for d in post_ratings]
            design_average = sum(design_ratings) / len(design_ratings)

            usability_ratings = [us.usability for us in post_ratings]
            usability_average = sum(usability_ratings) / len(usability_ratings)

            content_ratings = [content.content for content in post_ratings]
            content_average = sum(content_ratings) / len(content_ratings)

            score = (design_average + usability_average + content_average) / 3
            print(score)
            rate.design_average = round(design_average, 2)
            rate.usability_average = round(usability_average, 2)
            rate.content_average = round(content_average, 2)
            rate.score = round(score, 2)
            rate.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = RatingForm()
    params = {
        'post': post,
        'rating_form': form,
        'rating_status': rating_status

    }
    return render(request, 'rating.html', params)

@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'project' in request.GET and request.GET['project']:
        search_term =request.GET.get('project')
        searched_project = Project.search_by_title(search_term)
        message = f'{search_term}'

        return render(request, 'search.html',{"message":message,"projects":searched_project})

    else:
        message = "You haven't searched for any term"

        return render(request,'search.html',{'message':message})

@login_required(login_url='/accounts/login/')
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
 
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
 
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
 
    return render(request, 'profile.html', context)

@login_required(login_url='/accounts/login/')
def update_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user)
        if u_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('home')
 
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
 
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
 
    return render(request, 'update_profile.html', context)

@login_required(login_url='/accounts/login/')
def new_project(request):
    current_user = request.user
   
    if request.method == 'POST':
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
           
            image.save()
            
        return redirect('home')

    else:
        form = NewProjectForm()
    return render(request, 'new_project.html', {"form": form})

def home(request):
    project=Project.all_projects()
    user_projects = []
    for project in project:
        pic = Profile.objects.filter(user=project.user).first()
        if pic:
            pic = pic.image.url
        else:
            pic = ''
        obj = dict(
            title=project.title,
            url=project.url,
            image=project.image,
            avatar=pic,
            description=project.description,
            author=project.user,
            date_posted=project.date_posted,
            technologies = project.technologies,
        )
        user_projects.append(obj)

    return render(request, 'home.html',{"user_projects":user_projects})

# serializer views
class ProfileList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self,request,format=None):
        profiles = Profile.objects.all()
        serializers =ProfileSerializer(profiles,many=True)
        return Response(serializers.data)

class ProjectList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self,request,format=None):
        projects = Project.objects.all()
        serializers =ProjectSerializer(projects,many=True)
        return Response(serializers.data)
