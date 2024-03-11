from rest_framework.viewsets import ModelViewSet

from accounts.models import UserProfile, Post, Module, Enrollment, Feedback, MediaFile
from accounts.api.serializers import PostSerializer, UserProfileSerializer, ModuleSerializer, EnrollmentSerializer, FeedbackSerializer, MediaFileSerializer

class UserProfileViewset(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class PostViewset(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class ModuleViewset(ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

class EnrollmentViewset(ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class FeedbackViewset(ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class MediaFileViewset(ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer


