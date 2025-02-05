"""
URL configuration for quiz_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt import authentication
from django.urls import path, include,re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

schema_view = get_schema_view(
    openapi.Info(
        title="Quiz App Management API",
        default_version='v1',
        description="It Will Perform Crud Operations For Quiz App",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="veluruanirudh08@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    authentication_classes=(authentication.JWTAuthentication,),
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/',swagger_auto_schema(methods=['post'],security=[])(TokenObtainPairView.as_view())),
    path('api/token/refresh/',swagger_auto_schema(methods=['post'],security=[])(TokenRefreshView.as_view())),
    path('api/users/', include('users.urls')),
    path('api/quiz/', include('quiz.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
