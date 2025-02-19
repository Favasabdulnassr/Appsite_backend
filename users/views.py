from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerilizer,MyTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .permission import IsUser



class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = RegisterSerilizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Registration Completed Successfully'},status=status.HTTP_200_OK)

        print("Serializer errors",serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer





class UserPointsView(APIView):
    permission_classes = [IsUser]

    def get(self, request):
        user = request.user
        return Response({
            'total_points': user.total_points,
        }, status=status.HTTP_200_OK)