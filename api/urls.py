from django.contrib import admin
from django.urls import include, path
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.Signup.as_view()),
    path('login/', views.Login.as_view()),
    path('logout/', views.Logout.as_view()),
    path('profile/', views.GetOwnProfile.as_view()),
    path('search/', views.SearchCities.as_view()),
    path('user/cities/', views.get_user_cities),
    path('', views.Weather_Forecast_API.as_view())
]