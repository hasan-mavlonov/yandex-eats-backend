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
        response = self.client.post(reverse('login'), {'phone': '+998901115146'}, follow=False)
        self.assertEqual(response.status_code, 302)  # Expect redirection
        self.assertEqual(response.url, reverse('admin-login'))  # Ensure redirection URL is correct

    def test_user_login_redirects_to_phone_verification(self):
        response = self.client.post(reverse('login'), {'phone': '+998901115145'}, follow=False)
        self.assertEqual(response.status_code, 302)  # Expect redirection
        self.assertEqual(response.url, reverse('send-phone-verification-code'))  # Ensure correct redirection URL

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
        self.assertEqual(response.data['message'], 'Client logged in successfully!')


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

    def test_non_admin_login_redirects_to_verification(self):
        response = self.client.post(reverse('login'), {'phone': '+998990894981'})  # Use non-admin phone
        self.assertRedirects(response, reverse('send-phone-verification-code'))

    def test_admin_login_success(self):
        # Simulate login with the correct password (no need for phone in request anymore)
        response = self.client.post(reverse('admin-login'), {'password': 'saida0525'})

        # Assert that the response is successful with status code 200
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
        self.assertEqual(response.data['message'], 'Admin logged in successfully!')

    def test_admin_login_failure_wrong_password(self):
        # Admin login with incorrect password
        response = self.client.post(reverse('admin-login'), {'password': '123qwerty'}, follow=False)

        # Assert that the status code is 400 because the password is incorrect
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that the error message contains the expected invalid password message
        self.assertIn('Invalid password', str(response.data))
