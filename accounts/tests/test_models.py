from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from ..models import UserProfile, Module, Post, MediaFile, Enrollment, Feedback, Notification

class UserProfileModelTest(TestCase):
    def setUp(self):
        #create a test user and user profile
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            user_type='student',
            email='testuser@example.com'
        )

    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.user.username, 'testuser')
        self.assertEqual(self.user_profile.user_type, 'student')
        self.assertEqual(self.user_profile.email, 'testuser@example.com')


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #create a user and associated user profile
        test_user = User.objects.create_user(username='testuser', password='12345')
        test_user_profile = UserProfile.objects.create(
            user=test_user,
            user_type='student', 
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        
        #create a Post instance
        Post.objects.create(
            user=test_user_profile,
            content="This is a test post."
        )

    def test_content_field(self):
        post = Post.objects.get(id=1)
        expected_content = "This is a test post."
        self.assertEqual(post.content, expected_content)

    def test_user_link(self):
        post = Post.objects.get(id=1)
        expected_user = 'testuser'
        self.assertEqual(post.user.user.username, expected_user)

    def test_str_method(self):
        post = Post.objects.get(id=1)
        expected_string = f'{post.user.user.username} - {post.created_at}'
        self.assertEqual(str(post), expected_string)


class ModuleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='12345')
        user_profile = UserProfile.objects.create(user=user, user_type='teacher', email='test@example.com')

        Module.objects.create(teacher=user_profile, title="Test Module", content="Test content")

    def test_title_label(self):
        module = Module.objects.get(id=1)
        field_label = module._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_content_label(self):
        module = Module.objects.get(id=1)
        field_label = module._meta.get_field('content').verbose_name
        self.assertEqual(field_label, 'content')

    def test_teacher_label(self):
        module = Module.objects.get(id=1)
        field_label = module._meta.get_field('teacher').verbose_name
        self.assertEqual(field_label, 'teacher')

    def test_module_str_method(self):
        module = Module.objects.get(id=1)
        expected_object_name = module.title
        self.assertEqual(str(module), expected_object_name)


class MediaFileModelTest(TestCase):
    def setUp(self):
        #create a user and profile
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user, user_type='teacher')

        #create a module
        self.module = Module.objects.create(teacher=self.user_profile, title='Test Module', content='Test Content')

        #create a media file for the module
        self.media_file = SimpleUploadedFile(name='test_file.jpg', content=b'', content_type='image/jpeg')
        self.media_file_obj = MediaFile.objects.create(module=self.module, file=self.media_file)

    def test_media_file_creation(self):
        self.assertEqual(self.media_file_obj.module, self.module)
        self.assertTrue(self.media_file_obj.file, 'test_file.jpg')

    def test_module_association(self):
        self.assertEqual(self.media_file_obj.module.title, 'Test Module')
        self.assertEqual(self.media_file_obj.module.content, 'Test Content')

    def test_file_path(self):
        #check if the file path starts with the expected directory
        self.assertTrue(self.media_file_obj.file.name.startswith('module_media/'))
 
        self.assertIn('test_file', self.media_file_obj.file.name)
  
        self.assertTrue(self.media_file_obj.file.name.endswith('.jpg'))


class EnrollmentModelTest(TestCase):
    def setUp(self):
        #create a user and associated UserProfile
        self.student_user = User.objects.create_user(username='studentuser', password='12345')
        self.student_profile = UserProfile.objects.create(
            user=self.student_user,
            user_type='student',
            email='student@example.com'
        )

        #create a teacher and associated UserProfile
        self.teacher_user = User.objects.create_user(username='teacheruser', password='54321')
        self.teacher_profile = UserProfile.objects.create(
            user=self.teacher_user,
            user_type='teacher',
            email='teacher@example.com'
        )

        #create a module taught by the teacher
        self.module = Module.objects.create(
            teacher=self.teacher_profile,
            title='Test Module',
            content='This is a test module content'
        )

        #enroll the student in the module
        self.enrollment = Enrollment.objects.create(
            user=self.student_user,
            module=self.module
        )

    def test_enrollment_creation(self):
        self.assertEqual(self.enrollment.user, self.student_user)
        self.assertEqual(self.enrollment.module, self.module)

    def test_module_student_association(self):
        self.assertIn(self.student_user.id, self.module.enrollment_set.all().values_list('user', flat=True))

    def test_enrollment_count(self):
        enrollment_count = Enrollment.objects.filter(user=self.student_user).count()
        self.assertEqual(enrollment_count, 1)


class FeedbackModelTest(TestCase):

    def setUp(self):
        #create a user
        self.user = User.objects.create_user(username='testuser', password='12345')

        #create a user profile associated with the user
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            user_type='student',
            email='testuser@example.com',
            dob='2000-01-01',
            first_name='Test',
            last_name='User',
        )

        #create a module
        self.module = Module.objects.create(
            teacher=self.user_profile,  # Assuming a teacher can also be a student for simplicity
            title='Test Module',
            content='This is a test module.',
        )

        #create a feedback entry
        self.feedback = Feedback.objects.create(
            user=self.user,
            module=self.module,
            content='This is a test feedback.',
        )
    #test that the feedback content is correctly saved
    def test_feedback_content(self):
        
        self.assertEqual(self.feedback.content, 'This is a test feedback.')
    #test that the feedback is correctly associated with a user and a module
    def test_feedback_association(self):
        
        self.assertEqual(self.feedback.user, self.user)
        self.assertEqual(self.feedback.module, self.module)
        
