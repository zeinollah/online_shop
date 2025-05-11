from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import RegistrationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    metadata_class = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "User registered",},
             status=status.HTTP_201_CREATED
        )