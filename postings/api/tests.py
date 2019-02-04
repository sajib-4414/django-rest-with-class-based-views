from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from postings.models import BlogPost
from rest_framework.reverse import reverse as api_reverse
from rest_framework_jwt.settings import api_settings
payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER


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

    def test_get_list(self):
        data = {}
        url = api_reverse("api-postings:post-listcreate")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item(self):
        data = \
        {'title':'some rando title',\
         'content':'some more content'}
        url = api_reverse("api-postings:post-listcreate")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item(self):
        blog_post = BlogPost.objects.first()
        data = {}
        url = blog_post.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response)

    def test_update_item(self):
        blog_post = BlogPost.objects.first()
        url = blog_post.get_api_url()
        data = \
        {'title':'some rando title',\
         'content':'some more content'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item_with_user(self):
        blog_post = BlogPost.objects.first()
        print(blog_post.content)
        url = blog_post.get_api_url()
        data = \
        {'title':'some rando title',\
         'content':'some more content'}
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_response = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item_with_authorization(self):
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_response = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)
        data = \
            {'title': 'some rando title', \
             'content': 'some more content'}
        url = api_reverse("api-postings:post-listcreate")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_ownership(self):
        owner = User.objects.create(username='testuser2222')
        blog_post = BlogPost.objects.create(
            user=owner,
            title='New title',
            content='some random content')
        user_obj = User.objects.first()
        self.assertNotEqual(user_obj.username, owner.username)

        payload = payload_handler(user_obj)
        token_response = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)

        url = blog_post.get_api_url()
        data = \
            {'title': 'some rando title', \
             'content': 'some more content'}
        response = self.client.put(url, data,format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
