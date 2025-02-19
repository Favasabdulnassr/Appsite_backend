from django.urls import path
from .views import RegisterView,MyTokenObtainPairView,UserPointsView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('token/',MyTokenObtainPairView.as_view(),name='token'),
    path('token/refresh/',TokenRefreshView.as_view(),name='refreshToken'),
     path('points/', UserPointsView.as_view(), name='user-points'),  # New URL path


    
]
