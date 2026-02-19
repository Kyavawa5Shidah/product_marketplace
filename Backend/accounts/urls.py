from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RoleViewSet
from django.urls import path
from .views import EmailTokenObtainPairView, current_user
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('roles', RoleViewSet, basename='roles')

urlpatterns = [
    path('auth/login/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('current_user/', current_user, name='current_user'), 
]

urlpatterns += router.urls
