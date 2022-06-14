from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime as dt 
from django.db.models.signals import post_save
from django.dispatch  import receiver
from tinymce.models import HTMLField

from awards.serializer import ProjectSerializer
from awards.views import ProjectList

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=200,null=True,blank=True,default='')
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to = 'profile/',blank = 'True',default='default.png')
    
    def __str__(self):
        return f'{self.user.username} profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    def save_profile(sender, instance, **kwargs):
        instance.profile.save()

    
    post_save.connect(create_user_profile, sender=User)
    post_save.connect(save_profile, sender=User)


class Ratings(models.Model):
    design_average = models.FloatField(default=0, blank=True)
    usability_average = models.FloatField(default=0, blank=True)
    content_average = models.FloatField(default=0, blank=True)
    ratings=((1, '1 - poor'),(2, '2 - pathetic'),(3, '3 - very bad'),(4, '4 - bad'),(5, '5 - average'),(6, '6 - good'),(7, '7 - very good'),(8, '8 - perfect'),(9, '9 - exellent'),(10, '10 - genius',))
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='rater')
    design = models.IntegerField(choices=ratings, default=0, blank=True)
    usability = models.IntegerField(choices=ratings, blank=True, default=0)
    content = models.IntegerField(choices=ratings, blank=True,default=0)
    # comment = models.CharField(max_length=250, blank=True,default='')  
    score = models.FloatField(default=0, blank=True)
    # post = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings', null=True)


    def save_rating(self):
        self.save()
    
    def __str__(self):
        return f'{self.post} Rating'
    
    @classmethod
    def get_rating(cls, id):
        ratings = Ratings.objects.filter(post_id=id).all()
        return ratings     

class Project(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField(max_length=255)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    technologies = models.CharField(max_length=200, blank = True)
    image = models.ImageField(upload_to = 'images/',blank = True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default='',null=True ,related_name='author')


    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()

    @classmethod
    def all_projects(cls) :
        projects = cls.objects.all()
        return projects
        
    @classmethod
    def search_by_title(cls,search_term):
        projects = cls.objects.filter(title__icontains=search_term)
        return projects

    def __str__(self):
        return self.title