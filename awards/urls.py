from importlib.resources import path
from unicodedata import name
from django.urls import path
from awards.views import *
from awards import views
# from awards.views import  EditProfile
from django.conf import settings
from django.conf.urls.static import static
from awards import views as user_views


urlpatterns =[
    path('', views.home, name = 'home'),
    path('profile/', views.profile,name, name="profile"),
    path('search/', views.search_results, name = 'search_results'),
    path('update_profile/', user_views.update_profile,name = 'update_profile'),
    path('rating/<post>', views.p_rating, name='rating'),
    path('project/', views.new_project,name ='new_project'),
    path('api/profiles/',views.ProfileList.as_view()),
    path('api/projects/', views.ProjectList.as_view()),

    # User Authentication
    # path('sign-up/', views.register, name="sign-up"),
    # path('logout/', views.register, name='logout'),
    # path('search/', views.search, name='search'),
    # path('register/',views.register,name='register'),
    # path("profile/", views.profile, name="profile"),



]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

