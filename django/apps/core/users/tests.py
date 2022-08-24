from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from apps.core.users.models import User, Profile
from apps.core.users.serializers import RegisterSerializer

# Create your tests here.
class UserAppTest(APITestCase):
    def setUp(self):
        self.data = {
            "username": "hello@example.com",
            "password": "testpassword811",
            "password2": "testpassword811",
            "email": "hello@example.com",
            "first_name": "example first name",
            "last_name": "example last name",
            "organization": "example organization",
        }
        self.register_serializer = RegisterSerializer(data=self.data)
        self.register_serializer.is_valid()
        self.register_serializer.save()
        token = Token.objects.get(user__email=self.data["username"])
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")


    def test_user_register_serializer(self):
        u = User.objects.filter().count()
        p = Profile.objects.filter().count()
        t = Token.objects.filter().count()
        # check if other entries are created by signals.py
        self.assertEqual(u, p)
        self.assertEqual(u, t)

    def test_user_register_api(self):
        register_url = "/users/api/register"
        data = self.data.copy()
        data["username"] = "hello1@example.com"
        data["email"] = "hello1@example.com"
        response = self.client.post(register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        u = User.objects.filter()
        print(u)
        u_count = u.count()
        self.assertEqual(u_count, 2)

    def test_user_profile_api(self):
        profile_url = "/users/api/profile/"
        response = self.client.get(profile_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_subscriptions_api(self):
        subscriptions_url = "/users/api/subscriptions/"
        response = self.client.get(subscriptions_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
