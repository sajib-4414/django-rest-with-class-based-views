from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from postings.models import BlogPost


#automated
#new/blank db
class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        user = User(username='arefin', email='')
        user.set_password("python123456")
        user.save()
        blog_post = BlogPost.objects.create(
            user=user,
            title='New title',
            content='some new test created title')

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count,1)

    def test_single_post(self):
        post_count = BlogPost.objects.count()
        self.assertEqual(post_count,1)



