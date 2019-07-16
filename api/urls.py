from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet,base_name="posts")



urlpatterns=[
    path('users/',views.UserList.as_view(),name="user_list"),
    path('user/<int:pk>/',views.UserDetali.as_view(),name="user_detali"),
    path('user-create/',views.UserCreate.as_view(),name='user_create'),
    path('user-auth/',views.authenticate_user,name="user_auth"),
    path('',include(router.urls)),
    
]