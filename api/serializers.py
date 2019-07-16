from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Post
from . import likes_function
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            max_length=32,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
             validated_data['password'],is_active=1)
        return user

    class Meta:
        model=User
        fields='__all__'


class PostSerializer(serializers.ModelSerializer):
    is_fan=serializers.SerializerMethodField() 


    class Meta:
        model=Post
        fields=('title','body','pub_date','total_likes','is_fan')

    def get_is_fan(self, obj):
        user = self.context.get('request').user
        return likes_function.is_fan(obj, user)

class FanSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = (
            'username',
            'full_name',
        )
    def get_full_name(self, obj):
        return obj.get_full_name()
