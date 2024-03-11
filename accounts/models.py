from django.db import models
from django.contrib.auth.models import User

#user profiles model
class UserProfile(models.Model):
    #username and password field is default in Django's user model 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length = 10, choices=[('student','Student'),('teacher','Teacher')])
    email = models.EmailField(max_length=250)
    dob = models.DateField(null=True, blank=True)
    #using Djanog's built-in fields for first and last name
    first_name  = models.CharField(max_length = 50, blank=True)
    last_name  = models.CharField(max_length = 50, blank=True)
    profile_photo = models.FileField(upload_to='user_media/', null=True, blank=True)

#posts model, posts by all users are stored here
class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.user.username} - {self.created_at}'

#modules model
class Module(models.Model):
    teacher = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='modules')
    title = models.CharField(max_length=100)
    content = models.TextField() #description / content of modules
    image = models.ImageField(upload_to='module_media/', null=True, blank=True) #image field for module thumbnail

    def __str__(self):
        return self.title

#media files model, one module may have several media files
class MediaFile(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='media_files')
    file = models.FileField(upload_to='module_media/')

#enrollment model to record students and modules they enrolled in
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.module.title}"    
    
#feedback models to record all feedbacks on modules made by students
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.module.title} - {self.created_at}"

#notification models to keep and display notification records
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20)  
    sender_name = models.CharField(max_length=255) 
    item_title = models.CharField(max_length=255) 
    item_url = models.URLField(max_length=1024)  
    date_created = models.DateTimeField(auto_now_add=True)

