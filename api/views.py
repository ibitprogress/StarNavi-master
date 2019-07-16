from django.contrib.auth.models import User
from django.conf import settings
from .models import Post
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework import status,viewsets
from rest_framework_jwt.utils import jwt_payload_handler
import jwt
import json
import requests
import clearbit
from django.contrib.auth.signals import user_logged_in
from .serializers import UserSerializer, PostSerializer
from rest_framework.response import Response
from .likes_function import *
from .mixins import LikedMixin

class UserList(APIView):
    permission_classes=(AllowAny, )

    def get(self,request,format=None):
        users=User.objects.all()
        users=UserSerializer(users,many=True)
        return Response(users.data)

class UserDetali(APIView):
    permission_classes=[AllowAny, ]

    def get(self,request,pk,format=None):
        try: 
            user=User.objects.get(pk=pk)
        except User.DoesNotExist:
            user_count=User.objects.all().count()
            user=User.objects.get(pk=user_count)
        user=UserSerializer(user)
        return Response(user.data)


class UserCreate(APIView):
    permission_classes=(AllowAny, )

    def post(self, request, format=None):
        clearbit.key= "sk_4728885ed5d4127aa300ed72b4d6032b"
        serializer = UserSerializer(data=request.data)
        email_verification = requests.get('https://api.hunter.io/v2/email-verifier?email='+ request.data['email'] +'&api_key=18e9e8d17054963348e16dcdd43de534ee803661')
        email_verification = json.loads(email_verification.content)
        if serializer.is_valid() and email_verification['data']['webmail']:
            more_information = clearbit.Person.find(email=request.data['email'])
            serializer.first_name = more_information['name']['givenName']
            serializer.last_name = more_information['name']['familyName']
            user = serializer.save()
            if user:
                data = serializer.data
                return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
 
    try:
        username = request.data['username']
        password = request.data['password']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = 0
        auth = user.check_password(password)
        if auth:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details['name'] = "%s %s" % (
                    user.first_name, user.last_name)
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)
 
            except Exception as e:
                raise e

        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a username and a password'}
        return Response(res)





class PostViewSet(LikedMixin,viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    permission_classes=(IsAuthenticatedOrReadOnly,)

