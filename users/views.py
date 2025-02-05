from django.shortcuts import render
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegisterUserAPIView(APIView):
    """Create User for authentication."""
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


    @swagger_auto_schema(
        request_body=RegisterSerializer,
        query_serializer=RegisterSerializer,
        security=[],
    )
    def post(self, request):
        """Get request data & save."""
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            print(serializer.errors)
            return Response({
                'status':status.HTTP_400_BAD_REQUEST,
                'errors':serializer.errors,
                'message':'Invalid data'
            })

        serializer.save()
        return Response({
            'status':status.HTTP_201_CREATED,
            # 'data':serializer.data,
            'message':'User added successfully'
        })

class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

   
    def get(self, *args):
        user_obj = self.get_object()
        serializer = UserSerializer(user_obj)

        return Response(({
            'status':status.HTTP_200_OK,
            'data':serializer.data
        }))

    
    def patch(self, request):
        user_obj = self.get_object()
        serializer = UserSerializer(user_obj,data=request.data,partial=True)

        if not serializer.is_valid():
            return Response({
                'status':status.HTTP_400_BAD_REQUEST,
                'error':serializer.errors,
                'message':'Invalid data'
            })

        serializer.save()
        return Response(({
            'status':status.HTTP_200_OK,
            'message':'User partially updated successfully'
        }))

    
    def put(self, request):
        user_obj = self.get_object()
        serializer = UserSerializer(user_obj,data=request.data,partial=False)

        if not serializer.is_valid():
            return Response({
                'status':status.HTTP_400_BAD_REQUEST,
                'error':serializer.errors,
                'message':'Invalid data'
            })

        serializer.save()
        return Response(({
            'status':status.HTTP_200_OK,
            'message':'User updated successfully'
        }))
