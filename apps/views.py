from rest_framework import viewsets,status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser,FormParser,JSONParser
from django.shortcuts import get_object_or_404
from .models import AndroidApp,CompletedTask
from .serializers import AndroidAppSerializer,UserSerializer,CompletedTaskSerilizer
from users.permission import IsAdmin,IsUser
from users.models import CustomUser
import logging
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)

class AndroidAppViewSet(viewsets.ModelViewSet):
    queryset = AndroidApp.objects.all()
    serializer_class = AndroidAppSerializer
    parser_classes = (MultiPartParser, FormParser,JSONParser)  

    def get_permissions(self):
        permissions = []
        if self.action == 'list' or self.action == 'retrieve':  
            permissions = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy', 'update_points']: 
            permissions = [IsAdmin]
        return [permission() for permission in permissions]

  

    @action(detail=True,methods=['post'])
    def update_points(self,request,pk=None):
        app = self.get_object()
        points = request.data.get('points')

        if points is None:
            return Response({'error': 'Points value is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        app.points = points
        app.save()
        return Response({'message': 'Points updated successfully'})
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)
  
class CompletedTaskViewSet(viewsets.ModelViewSet):
    queryset = CompletedTask.objects.all()
    serializer_class = CompletedTaskSerilizer
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        if self.action in ['verify_task']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return CompletedTask.objects.all()
        return CompletedTask.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def verify_task(self, request, pk=None):
        task = self.get_object()
        if task.is_verified:
            return Response({'error': 'Task already verified'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        task.is_verified = True
        user = task.user
        user.total_points += 1
        user.save()
        task.save()
        
        
        return Response({'message': 'Task verified and points awarded'})
