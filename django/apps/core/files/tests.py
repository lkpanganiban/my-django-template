from django.core.files import File
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from apps.core.users.models import User, Subscriptions
from apps.core.users.serializers import RegisterSerializer
from .serializers import FileSetSerializer, FilesSerializer
from .models import FileSet, Files
from .actions import has_moderator_permissions, remove_moderator_permissions, fetch_fileset_moderator_permissions

# Create your tests here.
class FileAppTest(APITestCase):
    def _create_user(self, email="hello@example.com"):
        user_data = {
            "username": email,
            "password": "testpassword811",
            "password2": "testpassword811",
            "email": email,
            "first_name": "example first name",
            "last_name": "example last name",
            "organization": "example organization",
        }
        register_serializer = RegisterSerializer(data=user_data)
        register_serializer.is_valid()
        register_serializer.save()
        user_data["token"] = Token.objects.get(user__email=user_data["email"]).key
        return user_data

    def _create_file_set(self, user_data):
        user = User.objects.get(email=user_data["email"])
        subscription = Subscriptions.objects.filter(user_subscriptions__in=[user])
        # print(Subscriptions.objects.filter(user_subscriptions__in=[user]))
        set_data = {"subscription": str(subscription[0].id), "moderators": [str(subscription[0].owner.id)]}
        file_set_serializer = FileSetSerializer(data=set_data)
        file_set_serializer.is_valid()
        file_set_serializer.save()
        fs = FileSet.objects.all()[0].moderators.all()
        return file_set_serializer

    def _create_file(self, user_data, file_set_data):
        f = File(
            open("/usr/src/app/Dockerfile"), "rb"
        )  # cast io object with django file
        user = User.objects.get(email=user_data["email"])
        file_data = {
            "name": "dockerfile",
            "file_size": 100,
            "description": "description sample",
            "file_type": "pdf",
            "location": f,
            "file_set": file_set_data["id"],
            "owner": user.id,
        }
        file_serializer = FilesSerializer(data=file_data)
        file_serializer.is_valid()
        file_serializer.save()
        return file_serializer

    def setUp(self):
        self.user_data = self._create_user("hello@example.com")
        self.set_data = self._create_file_set(self.user_data)
        self.file_data = self._create_file(self.user_data, self.set_data.data)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user_data['token']}")

    def test_file_set_serializer(self):
        fset = FileSet.objects.filter().count()
        self.assertEqual(fset, 1)

    def test_file_set_get_api(self):
        file_set_url = "/files/api/set/"
        response = self.client.get(file_set_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["data"]), 1)

        # check file set ownership
        empty_user_data = self._create_user("hello2@example.com")
        empty_client = APIClient()
        empty_client.credentials(HTTP_AUTHORIZATION=f"Token {empty_user_data['token']}")
        empty_response = empty_client.get(file_set_url, format="json")
        self.assertEqual(len(empty_response.json()["data"]), 0)

    def test_subscription_access(self):
        file = Files.objects.filter()[0]
        u = User.objects.get(email=self.user_data["email"])
        self.assertTrue(file.has_subscription_access(u.user_subscriptions.all()[0]))
        # check file set ownership
        empty_user_data = self._create_user("hello2@example.com")
        u = User.objects.get(email=empty_user_data["email"])
        self.assertFalse(file.has_subscription_access(u.user_subscriptions.all()[0]))

    def test_destroy_fileset(self):
        for p in ["hello2@example.com", "hello3@example.com"]:
            user_data = self._create_user(p)
            set_data = self._create_file_set(user_data)
            self._create_file(user_data, set_data.data)
            self._create_file(user_data, set_data.data)
            
        file_set_url = "/files/api/set/"
        response = self.client.get(file_set_url, format="json")
        fs_id = response.json()["data"][0]["id"]
        file_set_url = f"/files/api/set/{fs_id}/"
        response = self.client.delete(file_set_url, format="json")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(FileSet.objects.all().count(), 2)
        self.assertEqual(Files.objects.all().count(), 4)

    def test_check_assign_moderator(self):
        user = User.objects.get(email=self.user_data["email"])
        set_data_id = self.set_data.data["id"]
        self.assertTrue(has_moderator_permissions(user, set_data_id))
        self.assertEqual(fetch_fileset_moderator_permissions(user).count(), 1)
        remove_moderator_permissions(user, set_data_id)
        self.assertFalse(has_moderator_permissions(user, set_data_id))
