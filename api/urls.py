from django.contrib import admin
from django.urls import include, path
# from rest_framework.routers import DefaultRouter

from accounts import views

# router = DefaultRouter()
# router.register('login', views.Login.as_view(), basename='login')
# router.register('register', views.Signup.as_view(), basename='register')
# router.register('logout', views.Logout.as_view(), basename='logout')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.Signup.as_view()),

    path('login/', views.Login.as_view()),
    path('logout/', views.Logout.as_view()),
]