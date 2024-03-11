from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Feedback, Module, MediaFile


#new user signups form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=250, help_text='Required. Enter a valid email address.')
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),help_text='Required. Enter your date of birth (YYYY-MM-DD)')
    user_type = forms.ChoiceField(choices=[('student','Student'),('teacher','Teacher')])
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'dob', 'user_type', 'first_name', 'last_name', 'password1', 'password2']

#posting updates/postsform 
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

#creating feedbacks form 
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['module', 'content']

    def __init__(self, user, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        enrolled_modules = Module.objects.filter(enrollment__user=user) # this filters the modules based on the enrolled modules of the logged in stuednt user
        self.fields['module'].queryset = enrolled_modules

#uploading new course materials form 
class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ['file']

#creating new course form 
class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'content', 'image']

#searching users form 
class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, label='Search Users')
