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
        data = {'title':'some rando title','content':'some more content'}
        url = api_reverse("api-postings:post-listcreate")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item(self):
        blog_post = BlogPost.objects.first()
        data = {}
        url = blog_post.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        blog_post = BlogPost.objects.first()
        url = blog_post.get_api_url()
        data = {'title':'some rando title', 'content':'some more content'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item_with_user(self):
        blog_post = BlogPost.objects.first()
        url = blog_post.get_api_url()
        data = {'title':'some rando title','content':'some more content'}
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
        data =  {'title': 'some rando title', 'content': 'some more content'}
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
        #this assertnotequal tests that the user we just created is not the
        #first user of the database
        self.assertNotEqual(user_obj.username, owner.username)

        #getting auth token for the first user in the database
        payload = payload_handler(user_obj)
        token_response = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)

        #trying to update the post as the first user, where the post was not
        #created by him, this post was created by the user we created in this
        #method
        url = blog_post.get_api_url()
        data = {'title': 'some rando title', 'content': 'some more content'}
        response = self.client.put(url, data,format='json')
        #it should give 403 error,because the user with whose token
        #we are trying to update is not the owner, only owner is permitted to update it
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_login_and_update(self):
        data = {
            'username':'arefin',
            'password':'python123456'
        }
        url = api_reverse('api-login')
        #this is just another way of getting the JWT auth token
        #previously in this file, we used two library methods to get the token
        #now are using another method for which we declared the url as auth/login
        #in project's url file
        response = self.client.post(url, data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        token = response.data.get('token')
        if token is not None:
            blog_post = BlogPost.objects.first()
            url = blog_post.get_api_url()
            data = {'title': 'some rando title', 'content': 'some more content'}

            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

            response = self.client.put(url, data, format='json')
            #update will give 200 because, we are pulling token
            #with the first user we created
            #and trying to update the first post with that user
            #where the user is essentially the owner
            self.assertEqual(response.status_code, status.HTTP_200_OK)


