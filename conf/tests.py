from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User


class LoginViewTest(TestCase):
    def setUp(self):
        # Set up the test client
        self.client = APIClient()

        # Create test users
        self.admin_user = User.objects.create(
            phone="+998901115146",
            name="Admin",
            role="super_admin",
            is_active=True,
            is_staff=True,
            is_superuser=True
        )

        self.client_user = User.objects.create(
            phone="+998901115145",
            name="Client",
            role="client",
            is_active=False,
            longitude=0.0,
            latitude=0.0
        )

    def test_user_login_redirects_to_admin_login(self):
        # Test if a staff user is redirected to the admin login page
        response = self.client.post(reverse('login'), {'phone': '+998901115146'})
        # The response should be a redirect to 'admin-login'
        self.assertRedirects(response, '/auth/admin/login')

    def test_user_login_redirects_to_phone_verification(self):
        # Test if a non-active user is redirected to send phone verification code
        response = self.client.post(reverse('login'), {'phone': '+998901115145'})
        # The response should be a redirect to 'send-phone-verification-code'
        self.assertRedirects(response, '/auth/send-phone-verification-code')

    def test_successful_user_login(self):
        # Create an active user for a successful login
        active_user = User.objects.create(
            phone="+998901115147",
            name="Active User",
            role="client",
            is_active=True,
            longitude=0.0,
            latitude=0.0
        )

        response = self.client.post(reverse('login'), {'phone': '+998901115147'})
        # The response should return the access and refresh tokens with status 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
        self.assertEqual(response.data['message'], 'client logged in successfully!')


class AdminLoginViewTest(TestCase):
    def setUp(self):
        # Set up the test client
        self.client = APIClient()

        # Create the admin user
        self.admin_user = User.objects.create(
            phone="+998901115146",
            name="Admin",
            role="super_admin",
            is_active=True,
            is_staff=True,
            is_superuser=True
        )

    def test_admin_login_success(self):
        # Admin login with the correct password
        response = self.client.post(reverse('admin-login'), {'password': 'saida0525'})
        # The response should return the access and refresh tokens with status 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
        self.assertEqual(response.data['message'], 'Admin logged in successfully!')

    def test_admin_login_failure_wrong_password(self):
        # Admin login with incorrect password
        response = self.client.post(reverse('admin-login'), {'password': 'wrongpassword'})
        # The response should be an error due to invalid password
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid password.')

    def test_admin_login_failure_no_admin_user(self):
        # Simulate that the admin user does not exist
        User.objects.filter(phone="+998901115146").delete()

        response = self.client.post(reverse('admin-login'), {'password': 'saida0525'})
        # The response should be an error due to no admin user found
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Admin user not found.')
