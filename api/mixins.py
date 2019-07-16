from rest_framework.decorators import detail_route
from rest_framework.response import Response
from . import likes_function as services
from .serializers import FanSerializer

class LikedMixin:
    @detail_route(methods=['POST'])
    def like(self, request, pk=None):

        obj=self.get_object()
        services.add_like(obj, request.user)
        return Response()
    @detail_route(methods=['POST'])
    def unlike(self, request, pk=None):
        
        obj=self.get_object()
        services.remove_like(obj, request.user)
        return Response()
    @detail_route(methods=['GET'])
    def fans(self, request, pk=None):
        obj = self.get_object()
        fans=services.get_fans(obj)
        serializer=FanSerializer(fans, many=True)
        return Response(serializer.data)