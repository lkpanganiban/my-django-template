from rest_framework import status
from rest_framework.test import APITestCase
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
        u_count = u.count()
        self.assertEqual(u_count, 2)
