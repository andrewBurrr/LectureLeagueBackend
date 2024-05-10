from django.shortcuts import render
from .models import CustomUser
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomUserCreateSerializer, CustomTokenObtainPairSerializer, CustomUserSerializer


# # Create your views here.
# class CreateUserView(generics.CreateAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = CustomUserCreateSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             self.perform_create(serializer)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class UserAccountViewSet(viewsets.ModelViewSet):

    """
    Viewset to provide the following CRUD operations for the custom user model:
            - Retrieve
            - Update
            - Delete
    For use by the user for viewing and updating their profile.
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        """Instantiates and returns the list of permissions that this view requires."""
        if self.action == 'create':
            permission_classes = [AllowAny()]
        else:
            permission_classes = [IsAuthenticated()]
        return [permission() for permission in permission_classes]
    
    def create(self, request):
        serializer = CustomUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST


    def retrieve(self, request, pk=None):
        user = self.get_object()
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def update(self, request, pk=None):
        user = self.get_object()
        serializer = CustomUserSerializer(user, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def partial_update(self, request, pk=None):
        user = self.get_object()
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_200_OK)
    

# class PublicUserViewSet(viewsets.ModelViewSet):
#     """
#     Viewset to provide the following CRUD operations for the custom user model:
#             - Retrieve
#     For use by the user for viewing other user's profiles.
#     """

#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer

#     def get_permissions(self):
#         """Instantiates and returns the list of permissions that this view requires."""
#         permission_classes = [AllowAny()]
#         return [permission() for permission in permission_classes]

#     def retrieve(self, request, pk=None):
#         user = self.get_object()
#         serializer = CustomUserSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)