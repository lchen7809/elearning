from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from accounts.models import UserProfile, Post, Module, Enrollment, Feedback, MediaFile


class UserProfileSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    # profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['user_username', 'email', 'first_name', 'last_name', 'dob', 'user_type', 'profile_photo']
        extra_kwargs = {
            'user': {'read_only': True},
        }


class PostFormSerializer(serializers.Serializer):
    content = serializers.CharField()

    def create(self, validated_data):
        user_profile = self.context['request'].user.userprofile
        post = Post.objects.create(user=user_profile, **validated_data)
        return post

class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z", read_only=True)

    class Meta:
        model = Post
        fields = ['content', 'created_at']

class ModuleSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = '__all__'  # Adjust this as necessary

    def get_teacher_name(self, obj):
        # Assuming the teacher's name is composed of first_name and last_name
        return f"{obj.teacher.first_name} {obj.teacher.last_name}"


class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'