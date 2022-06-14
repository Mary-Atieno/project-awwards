from django.test import TestCase
from .models import Profile,Project,Ratings
from django.contrib.auth.models import User
import unittest
# # Create your tests here.
class TestProfile(TestCase):
    def setUp(self):
        self.e_user = User(username="mary",email="mary@gmail.com",password="awwards")
        self.e_user.save()
        self.e_profile=Profile(user=self.e_user,bio="coding be my daily take",image="../images/default.png")

    def test_profile_instance(self):
        self.assertTrue(isinstance(self.e_profile, Profile))

class TestUser(TestCase):
    def setUp(self):
        self.e_user = User(username="mary",email="mary@gmail.com",password="awwards")
        self.e_user.save()

    def test_user_instance(self):
        self.assertTrue(isinstance(self.e_user, User))

class TestProject(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, username='mary')
        self.post = Project.objects.create(id=1, title='import error', image='../images/default.png', description='circulation import error',user=self.user, url='https://medium.com/@dibaekhanal101/cannot-import-name-modelname-from-partially-initialized-module-most-likely-due-to-a-circular-ee4c6ae51d7')

    def test_instance(self):
        self.assertTrue(isinstance(self.post, Project))

    def test_save_post(self):
        self.post.save_project()
        post = Project.objects.all()
        self.assertTrue(len(post) > 0)

    def test_get_posts(self):
        self.post.save()
        posts = Project.all_projects()
        self.assertTrue(len(posts) > 0)

    def test_search_post(self):
        self.post.save()
        post = Project.search_by_title('import error')
        self.assertTrue(len(post) > 0)

    def test_delete_post(self):
        self.post.delete_project()
        post = Project.search_by_title('import error')
        self.assertTrue(len(post) < 1)

class TestRating(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, username='mary')
        self.post = Project.objects.create(id=1, title='error', image='../images/default.png',url="https://medium.com/@dibaekhanal101/cannot-import-name-modelname-from-partially-initialized-module-most-likely-due-to-a-circular-ee4c6ae51d7", description='coding is fun',user=self.user)
        self.rating = Ratings.objects.create(id=1,usability=9,content = 9, design=8,user=self.user, post=self.post)

    def test_instance(self):
        self.assertTrue(isinstance(self.rating, Ratings))

    def test_save_rating(self):
        self.rating.save_rating()
        rating = Ratings.objects.all()
        self.assertTrue(len(rating) > 0)

    def test_get_rating(self,id):
        self.rating.save()
        rating = Ratings.get_rating(post_id=id)
        self.assertTrue(len(rating) == 1)

if __name__ == '__main__':
    unittest.main()