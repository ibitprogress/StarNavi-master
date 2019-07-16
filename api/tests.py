from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Post
from rest_framework_jwt.utils import jwt_encode_handler,jwt_payload_handler
from rest_framework import status

class AccountsTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user. 
        self.test_user = User.objects.create_user('testuser', 'test@gmail.com', 'testpassword')

        # URL for creating an account.
        self.create_url = reverse('user_create')

    def test_create_user(self):
      
        data = {
            'username': 'foobar',
            'email': 'l.luzhnuy@gmail.com',
            'password': 'somepassword'
        }

        response = self.client.post(self.create_url , data, format='json')
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)
   
    def test_create_user_with_short_password(self):
        data = {
                'username': 'foobar',
                'email': 'l.luzhnuy@gmai.com',
                'password': 'foo'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):
        data = {
                'username': 'foobar',
                'email': 'l.luzhnuy@gmai.com',
                'password': ''
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_too_long_username(self):
        data = {
            'username': 'foo'*30,
            'email': 'l.luzhnuy@gmai.com',
            'password': 'foobar'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_no_username(self):
        data = {
                'username': '',
                'email': 'l.luzhnuy@gmai.com',
                'password': 'foobar'
                }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_username(self):
        data = {
                'username': 'testuser',
                'email': 'turupuru8@gmail.com',
                'password': 'testuser'
                }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_email(self):
        data = {
            'username': 'testuser2',
            'email': 'test@gmail.com',
            'password': 'testuser'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_invalid_email(self):
        data = {
            'username': 'foobarbaz',
            'email':  'testing',
            'passsword': 'foobarbaz'
        }


        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_no_email(self):
        data = {
                'username' : 'foobar',
                'email': '',
                'password': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_auth(self):
        data={
            'username' : 'testuser',
            'password' : 'testpassword'
        }
        response=self.client.post(reverse('user_auth'),data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
    

    def test_user_list(self):
        response=self.client.get(reverse('user_list'),format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user(self):
        response=self.client.get('/api/user/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PostsTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword',is_active=1)
        
        self.test_post = Post.objects.create(user=self.test_user,title='hello',body="text text text text text text text text text text text text text text")
        payload = jwt_payload_handler(self.test_user)
        token = jwt_encode_handler(payload)
        self.auth = "JWT {}".format(token)

        self.base_url = reverse('posts-list')



    def test_post_list(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_post(self):
        response = self.client.get('/api/posts/1/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_create_post(self):
        data = {
            'user_id':self.test_user.id,
            'title':'hellllo',
            'body':'text text text text text text te4xt text 3text tex2t text tex1t text1 text1'
        }
        
        response = self.client.post(self.base_url, data, HTTP_AUTHORIZATION=self.auth, format=None)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_like_post(self):
        response=self.client.post(
            '/api/posts/1/like/',
            HTTP_AUTHORIZATION=self.auth,
            format=None
        )
        response_post = self.client.get('/api/posts/1/')
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response_post.data['total_likes'],1)
    

    def test_get_users_who_liked_post(self):
        self.client.post(
            '/api/posts/1/like/',
            HTTP_AUTHORIZATION=self.auth,
            format=None
        )
        response=self.client.get('/api/posts/1/fans/',HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data[0]['username'],'testuser')

    def test_unlike_post(self):
        response=self.client.post(
            '/api/posts/1/unlike/',
            HTTP_AUTHORIZATION=self.auth,
            format=None
        )
        response_post = self.client.get('/api/posts/1/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response_post.data['total_likes'],0)
