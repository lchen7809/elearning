from django.urls import path, include
from rest_framework.routers import SimpleRouter

from accounts.api import viewsets, views

router = SimpleRouter()
router.register(r'posts', viewsets.PostViewset, basename='post')


urlpatterns = [
    path('ping/', views.PingView.as_view(), name='ping'),
] + router.get_urls()
