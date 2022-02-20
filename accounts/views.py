from pickle import FALSE, TRUE
from django.contrib.auth import authenticate, get_user_model
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from accounts.models import UserProfile, ResearchedCities
from accounts.serializers import ProfileSerializer, SearchSerializer, SignupSerializer, LoginSerializer

class Weather_Forecast_API(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        return Response(
            [
                """Descrição : Essa API tem como intuito o registro de usuários e de pesquisas feitas por eles. Nessas pesquisas o foco foi o registro de cidades""",
                "e suas respectivas latitudes e longitudes, para serem usadas no projeto https://github.com/JoseCarlos33/weather-forecast-app-react-native",
                {
                    "Endpoints": [
                        {"Login": "https://drf-weather-forecast-app.herokuapp.com/login/"},
                        {"Cadastro": "https://drf-weather-forecast-app.herokuapp.com/register/"},
                        {"Registrar Pesquisas do Usuário Logado": "https://drf-weather-forecast-app.herokuapp.com/search/"},
                        {"Listar Pesquisas do Usuário Logado": "https://drf-weather-forecast-app.herokuapp.com/user/cities/"},
                        {"Listar Perfil do Usuário Logado": "https://drf-weather-forecast-app.herokuapp.com/profile/"},
                    ]
                }
            ]
        )

class BaseView(APIView):
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [IsAuthenticated,]

class Signup(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
   
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
    serializer_class = LoginSerializer

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
 
class GetOwnProfile(BaseView):

    def get(self, request):
        if request.META['HTTP_AUTHORIZATION']:
            token = request.META['HTTP_AUTHORIZATION'].split()
            email = Token.objects.get(key=token[1]).user
            user = UserProfile.objects.filter(email=email)
            serializer = ProfileSerializer(user, many=FALSE)
            return Response(serializer.data[0])
        else:
            content = {'detail':
                        'Forneça o token de autenticação no header da requisição para acessar as informações do seu perfil'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    
class SearchCities(BaseView):

    queryset = ResearchedCities.objects.all()
    serializer_class = SearchSerializer

    def post(self, request, format=None):
        token = request.META['HTTP_AUTHORIZATION'].split()
        email = Token.objects.get(key=token[1]).user
        user = UserProfile.objects.filter(email=email)
        user_serialized = ProfileSerializer(user, many=FALSE)
       
        serializer = self.serializer_class(data=
            {
                'user': user_serialized.data[0]['id'], 
                'city_name': request.data['city_name'],
                'latitude': request.data['latitude'],
                'longitude': request.data['longitude'],
            }
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_cities(request, format=None):
    
    if request.META['HTTP_AUTHORIZATION']:
        token = request.META['HTTP_AUTHORIZATION'].split()
        email = Token.objects.get(key=token[1]).user
        user = UserProfile.objects.filter(email=email)
        user_serialized = ProfileSerializer(user, many=FALSE)
        index_for_filter = user_serialized.data[0]['id']

        current_user_cities = ResearchedCities.objects.filter(user=index_for_filter)
        serializer = SearchSerializer(current_user_cities, many=TRUE)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        
        content = {'detail':
                    'Forneça o token de autenticação no header da requisição para acessar as informações do seu perfil'}
        return Response(content)