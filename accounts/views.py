from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import (RegistrationSerializer,
                          UpdateUserSerializer)
from .permissions import CurrentUserOrAdmin




User = get_user_model()

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    http_method_name = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "User registered",},
             status=status.HTTP_201_CREATED
        )

class UpdateUserViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [CurrentUserOrAdmin]

    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
             {"message": "User account updated",},
                   status=status.HTTP_200_OK
        )

















# class ProfileViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = User.objects.all()
#     serializer_class = RegistrationSerializer
#     http_method_names = ['get', 'put', 'patch', 'delete']
#
#     def get_queryset(self):
#         if self.request.user.is_superuser:
#             return User.objects.all()
#         else:
#             User.objects.filter(user = self.request.user)