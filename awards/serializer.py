from rest_framework import serializers
from .models import Project, Profile
from django.contrib.auth.models import User

# create models class
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['title','description','id','technologies','user','image','date_posted']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user','date','image','location','bio']
