from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.contrib.auth import authenticate
from .models import User, Role, Business
from .serializers import UserSerializer, RoleSerializer
from .permissions import IsBusinessAdmin
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from .serializers import EmailTokenObtainPairSerializer
from rest_framework.decorators import api_view, permission_classes


class CreateRoleView(generics.CreateAPIView):
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsBusinessAdmin]

    def get_queryset(self):
        return Role.objects.filter(business=self.request.user.business)

    def perform_create(self, serializer):
        serializer.save(business=self.request.user.business)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsBusinessAdmin]

    def get_queryset(self):
        return User.objects.filter(business=self.request.user.business)
    


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsBusinessAdmin]

    def get_queryset(self):
        return User.objects.filter(business=self.request.user.business)

    def perform_create(self, serializer):
        serializer.save(business=self.request.user.business)


class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsBusinessAdmin]

    def get_queryset(self):
        return Role.objects.filter(business=self.request.user.business)

    def perform_create(self, serializer):
        serializer.save(business=self.request.user.business)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)