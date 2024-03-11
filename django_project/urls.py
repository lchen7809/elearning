"""
URL configuration for django_project project.

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
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static



from rest_framework.routers import SimpleRouter
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from accounts.api import viewsets, views

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="E-Learn API",
        default_version = '1.0.0',
        description="API documentation of APP",
    ),
    public=True,
)



urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', include('accounts.urls')),
    path('',
         include([
             path('accounts/', include(('accounts.api.urls', 'accounts'), namespace='accounts')),
             path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
         ])),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
