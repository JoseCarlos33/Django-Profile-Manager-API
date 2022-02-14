
from django.contrib.auth import authenticate, get_user_model

from rest_framework import status, generics, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts import models, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from django.http import JsonResponse

from accounts.models import UserProfile
from accounts.serializers import ProfileSerializer

class BaseView(APIView):
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [IsAuthenticated,]

class Signup(APIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.SignupSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        print(serializer)
        if serializer.is_valid():
            name = serializer.data['name']
            current_city = serializer.data['current_city']
            email = serializer.data['email']
            password = serializer.data['password']

            try:
                user = get_user_model().objects.get(email=email)
                if user:
                    content = {'detail': 'Este email ja foi cadastrado.'}
                    return Response(content)

            except get_user_model().DoesNotExist:
                user = get_user_model().objects.create_user(email=email)

            # Set user fields provided
            user.set_password(password)
            user.name = name
            user.current_city = current_city
            user.save()


            content = {'name': name, 'email': email,
                       'current_city': current_city}

            return Response(content, status=status.HTTP_201_CREATED)

        return Response(serializer.errors)

class Login(APIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(email=email, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key},
                                status=status.HTTP_200_OK)
            else:
                content = {'detail':
                           'Unable to login with provided credentials.'}
                return Response(content, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class Logout(BaseView):

    def get(self, request, format=None):
        tokens = Token.objects.filter(user=request.user)
        for token in tokens:
            token.delete()
        content = {'success': 'User logged out.'}
        return Response(content, status=status.HTTP_200_OK)
 
class GetOwnProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.META['HTTP_AUTHORIZATION'].split()
        email = Token.objects.get(key=token[1]).user
        user = UserProfile.objects.filter(email=email)
        serializer = ProfileSerializer(user, many=True)
        return Response(serializer.data)

    
    