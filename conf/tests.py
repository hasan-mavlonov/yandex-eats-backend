from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User


class LoginViewTest(TestCase):
    def setUp(self):
        # Set up the test client
        self.client = APIClient()

        # Create an admin user (phone = +998901115146) and a regular user
        self.admin_user = User.objects.create_user(
            phone="+998901115146",
            password="saida0525",
            name="Admin",
            role="company_manager",  # Set as admin
            is_staff=True,
            is_superuser=True
        )

        self.client_user = User.objects.create_user(
            phone="+998901115145",
            password="clientpassword",
            name="Client",
            role="client",
            is_active=False,
            longitude=0.0,
            latitude=0.0
        )

    def test_user_login_redirects_to_admin_login(self):
        # Test if a user with phone '+998901115146' (admin) is redirected to admin login
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
        active_user = User.objects.create_user(
            phone="+998901115147",
            password="activepassword",
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

        # Create an admin user
        self.admin_user = User.objects.create_user(
            phone="+998901115146",
            password="saida0525",
            name="Admin",
            role="company_manager",
            is_active=True,
            is_staff=True,
            is_superuser=True
        )

    def test_admin_login_success(self):
        # Test admin login with the correct password 'saida0525'
        # First, simulate the login by phone
        response = self.client.post(reverse('login'), {'phone': '+998901115146'})
        # Check if the user is redirected to the admin login page
        self.assertRedirects(response, '/auth/admin/login')

        # Now, simulate the admin login using the correct password
        response = self.client.post(reverse('admin-login'), {'password': 'saida0525'})
        # The response should return the access and refresh tokens with status 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
        self.assertEqual(response.data['message'], 'Admin logged in successfully!')

    def test_admin_login_failure_wrong_password(self):
        # Admin login with incorrect password
        response = self.client.post(reverse('login'), {'phone': '+998901115146'})

