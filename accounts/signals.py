from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Module, MediaFile



print("Connecting post_migrate signal")

@receiver(post_migrate)
def load_dummy_data(sender, **kwargs):
    #this checks if the UserProfile model has been created
    try:
        profile_model = UserProfile._meta
    except:
        return
    

    if sender.name == 'accounts':
        #creating dummy data
        users_data = [
            {'username': 'student1', 'password': 'password123', 'user_type': 'student', 'email': 'student1@dummy.com', 'dob': '2000-01-01', 'first_name': 'Lizz', 'last_name': 'Johnson'},
            {'username': 'student2', 'password': 'password123', 'user_type': 'student', 'email': 'student2@dummy.com', 'dob': '2002-02-09', 'first_name': 'Jane', 'last_name': 'Austin'},
            {'username': 'student3', 'password': 'password123', 'user_type': 'student', 'email': 'student3@dummy.com', 'dob': '2001-12-03', 'first_name': 'Jack', 'last_name': 'Doe'},
            {'username': 'student4', 'password': 'password123', 'user_type': 'student', 'email': 'student4@dummy.com', 'dob': '2002-05-14', 'first_name': 'Meredith', 'last_name': 'Swith'},
            {'username': 'student5', 'password': 'password123', 'user_type': 'student', 'email': 'student5@dummy.com', 'dob': '2000-07-08', 'first_name': 'Chris', 'last_name': 'Dawnson'},
            {'username': 'teacher1', 'password': 'password123', 'user_type': 'teacher', 'email': 'teacher1@dummy.com', 'dob': '1985-05-15', 'first_name': 'James', 'last_name': 'Alec'},
            {'username': 'teacher2', 'password': 'password123', 'user_type': 'teacher', 'email': 'teacher2@dummy.com', 'dob': '1980-07-07', 'first_name': 'Rose', 'last_name': 'Smith'},
        ]

        for user_data in users_data:
            #this checks if the user already exists
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(username=user_data['username'], password=user_data['password'])
                UserProfile.objects.create(
                    user=user,
                    user_type=user_data['user_type'],
                    email=user_data['email'],
                    dob=user_data['dob'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                )
        
        #creating modules dummy data
        module_data = [
            {'username':'teacher1','title': 'Advanced Web Development', 'content': 'The module introduces a variety of topics around contemporary web server programming', 'image': 'awd_img.jpeg'},
            {'username':'teacher1','title': 'Machine Learning', 'content': 'This course provides a broad view of machine learning and neural networks. ', 'image':'ML_img.jpeg'},
            {'username':'teacher2','title': '3D Graphics & Animation', 'content': 'Develop basic but complete graphics software systems', 'image':'3D_img.png'},
            {'username':'teacher2','title': 'Data Science', 'content': 'Understand the scope and impact of Data Scienc', 'image':'DS_img.webp'},
        ]

        #creating media files associated with the module
        media_files_info = [
            {'file': 'AWD.pdf', 'module_title': 'Advanced Web Development'},
            {'file': 'ML.pdf', 'module_title': 'Machine Learning'},
            {'file': '3D.pdf', 'module_title': '3D Graphics & Animation'},
            {'file': 'DS.pdf', 'module_title': 'Data Science'},
        ]

        for module_info in module_data:
            teacher = UserProfile.objects.get(user__username=module_info['username'])
            if not Module.objects.filter(title=module_info['title']).exists():
                module = Module.objects.create(
                    teacher=teacher,
                    title=module_info['title'],
                    content=module_info['content'],
                    image=module_info['image']
                )
                

            for media_info in media_files_info:
                if not MediaFile.objects.filter(file=media_info['file']).exists():
                    #this checks if the media file is associated with the current module title
                    if media_info['module_title'] == module_info['title']:
                        MediaFile.objects.get_or_create(module=module, file=media_info['file'])

