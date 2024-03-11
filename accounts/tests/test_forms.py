from django.test import TestCase
from django.contrib.auth.models import User

from ..models import UserProfile, Module, Enrollment
from ..forms import SignUpForm, FeedbackForm

class SignUpFormTest(TestCase):
    def test_signup_form_valid(self):
        form_data = {'username': 'newuser', 
                     'email': 'newuser@example.com', 
                     'dob':'2000-01-01',
                     'user_type': 'student',
                     'first_name':'firstname',
                     'last_name':'lastname',
                     'password1': 'testpassword', 
                     'password2': 'testpassword'
                     }
        
        form = SignUpForm(data=form_data)
        if not form.is_valid():
            print("Form errors (expected form to be valid):", form.errors)
        self.assertTrue(form.is_valid())

    #intentionally invalid data for sign up 
    def test_signup_form_invalid(self):
        form_data = {'username': 'newuser', 
                     'email': 'newuserexample.com', 
                     'dob':'2000',
                     'user_type': 'student',
                     'first_name':'firstname',
                     'last_name':'lastname',
                     'password1': 'password', 
                     'password2': 'testpassword', 
                    }        
        form = SignUpForm(data=form_data)    
        self.assertFalse(form.is_valid())


class FeedbackFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #create test user and profiles
        cls.student_user = User.objects.create_user(username='studentuser', password='12345')
        cls.student_profile = UserProfile.objects.create(
            user=cls.student_user,
            user_type='student',
            email='student@example.com',
            dob='2000-01-01',
            first_name='Student',
            last_name='User',
        )
        
        cls.teacher_user = User.objects.create_user(username='teacheruser', password='54321')
        cls.teacher_profile = UserProfile.objects.create(
            user=cls.teacher_user,
            user_type='teacher',
            email='teacher@example.com',
            dob='1980-01-01',
            first_name='Teacher',
            last_name='User',
        )
        
        #create a test module and enroll the student
        cls.module = Module.objects.create(
            teacher=cls.teacher_profile,
            title='Test Module',
            content='Test content',
        )
        Enrollment.objects.create(user=cls.student_user, module=cls.module)

    def test_feedback_form_valid_data(self):
        form_data = {
            'module': self.module.id,
            'content': 'This is a test feedback.'
        }
        form = FeedbackForm(self.student_user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_feedback_form_invalid_module(self):
        another_module = Module.objects.create(
            teacher=self.teacher_profile,
            title='Another Module',
            content='More test content',
        )
        form_data = {
            'module': another_module.id,
            'content': 'This feedback should not be valid.'
        }
        form = FeedbackForm(self.student_user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('module', form.errors) 
