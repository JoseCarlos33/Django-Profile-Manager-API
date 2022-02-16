from django.contrib import admin
from django.urls import include, path
from accounts import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.Signup.as_view()),
    path('login/', views.Login.as_view()),
    path('logout/', views.Logout.as_view()),
    path('profile/', views.GetOwnProfile.as_view()),
    path('search/', views.SearchCities.as_view())
]