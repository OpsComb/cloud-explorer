from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class ECSClusterViewSet(viewsets.ViewSet):
    # serializer_class = ECSClusterSerializer
    lookup_field = 'name'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [IsAuthenticated]
        if self.action in ('update', 'delete', 'create'):
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request):
        return Response({"dummy": True})

    def create(self, request):
        return Response({"created": True})

    def retrieve(self, request, name):
        return Response({"name": name})

    def update(self, request, name):
        return Response({"updated": True})

    def partial_update(self, request, name=None):
        return Response({"updated": True})

    def destroy(self, request, name=None):
        return Response({"destroyed": True})


class ECSServiceViewSet(viewsets.ViewSet):
    # serializer_class = ECSServiceSerializer
    lookup_field = 'name'

    def list(self, request, *args, **kwargs):
        return Response({"dummy": "Service"})

    def retrieve(self, request, name=""):
        return Response({"dummy": "Service"})

    def update(self, request, name):

        return Response({"dummy": "Service"})


class ECSTaskViewSet(viewsets.ViewSet):
    # serializer_class = ECSTaskSerializer
    lookup_field = 'name'
