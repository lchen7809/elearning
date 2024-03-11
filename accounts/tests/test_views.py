from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import UserProfile, Notification

class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        UserProfile.objects.create(user=self.user, user_type='student', email='testuser@example.com')


    def test_dashboard_view_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view_unauthenticated(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/accounts/login/?next=/dashboard/')



class SearchResultsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.teacher_user = User.objects.create_user(
            username='teacheruser', 
            password='12345',
            first_name='Teacher',
            last_name='User'
        )
        cls.student_user = User.objects.create_user(
            username='studentuser', 
            password='12345',
            first_name='Student',
            last_name='User'
        )

        cls.teacher_profile = UserProfile.objects.create(
            user=cls.teacher_user,
            user_type='teacher',
            email='teacher@example.com',
        )
        cls.student_profile = UserProfile.objects.create(
            user=cls.student_user,
            user_type='student',
            email='student@example.com',
        )

    def test_search_results_with_query(self):
        #login as teacher to perform the search
        self.client.login(username='teacheruser', password='12345')

        #perform a search for the 'studentuser' username
        response = self.client.get(reverse('search_results'), {'search_query': 'studentuser'})

        #check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        #check if the search results contain 'studentuser'
        self.assertContains(response, 'studentuser')

        #check if the search results template is used
        self.assertTemplateUsed(response, 'teacher/search_results.html')

    def test_search_results_no_query(self):
        #login as teacher to perform the search
        self.client.login(username='teacheruser', password='12345')

        #perform a search without a query
        response = self.client.get(reverse('search_results'), {'search_query': ''})

        #check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        #check if the search results are empty
        self.assertNotContains(response, 'studentuser')
        self.assertNotContains(response, 'teacheruser')



class UserNotificationsViewTest(TestCase):
    def setUp(self):
        #create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')

        #create some notifications for the user
        Notification.objects.create(recipient=self.user, notification_type='new_course', sender_name='Admin', item_title='New Course Available', item_url='http://example.com/new_course')
        Notification.objects.create(recipient=self.user, notification_type='new_enrollment', sender_name='Student1', item_title='You have a new student', item_url='http://example.com/student_profile')

        #create a client to make requests
        self.client = Client()

    def test_user_notifications_authenticated(self):
        #log in as the test user
        self.client.login(username='testuser', password='12345')

        #make a GET request to the user_notifications view
        response = self.client.get(reverse('user_notifications'))

        #check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        #check that the context contains the notifications for the user
        notifications_in_context = response.context['notifications']
        self.assertEqual(notifications_in_context.count(), 2)
        self.assertTrue(all(notification.recipient == self.user for notification in notifications_in_context))

    def test_user_notifications_unauthenticated(self):
        #make a GET request to the user_notifications view without logging in
        response = self.client.get(reverse('user_notifications'))

        #check that the response redirects to the login page
        self.assertRedirects(response, f'/accounts/login/?next={reverse("user_notifications")}')