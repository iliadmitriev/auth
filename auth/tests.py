import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class UserDetailViewSetTest(TestCase):
    api_client = APIClient()

    def test_api_user_detail_get_403_no_auth(self):
        response = self.api_client.get(reverse("user_detail"))
        self.assertEqual(response.status_code, 403)

    def test_reg_and_user_detail_get_200_auth(self):
        login = "biguniqueemail123123@mail.ru"
        password = "321123"
        reg = self.api_client.post(
            reverse("register"),
            {
                "email": login,
                "password": password,
                "password2": password,
            },
        )
        self.assertEqual(reg.status_code, 201)
        token = self.api_client.post(reverse("token_obtain_pair"), {"username": login, "password": password})
        self.assertEqual(token.status_code, 200)
        self.assertIn("refresh", token.data)
        self.assertIn("access", token.data)
        access_token = token.data["access"]
        self.api_client.credentials(HTTP_AUTHORIZATION="Bearer %s" % access_token)
        response = self.api_client.get(reverse("user_detail"))
        self.assertEqual(response.status_code, 200)
        self.api_client.credentials()

    def test_reg_password_dont_match(self):
        login = "123biguniqueemail123123@mail.ru"
        password = "321123"
        password2 = "123321"
        reg = self.api_client.post(
            reverse("register"),
            {
                "email": login,
                "password": password,
                "password2": password2,
            },
        )
        self.assertEqual(reg.status_code, 400)


class TokenSuperUserViewSetTest(TestCase):
    api_client = APIClient()

    def test_generate_token_for_superuser(self):
        password = "secret_password"
        login = "adminuser"
        User.objects.create_superuser(login, "myemail@exampler.com", password)
        admin_token = self.api_client.post(reverse("token_obtain_pair"), {"username": login, "password": password})
        self.assertEqual(admin_token.status_code, 200)
        self.assertIn("access", admin_token.data)
        access_token = admin_token.data["access"]
        decoded_payload = jwt.decode(access_token, settings.SECRET_KEY, ["HS256"])
        self.assertIn("scope", decoded_payload)
        self.assertEqual(decoded_payload["scope"], "admin")
        self.api_client.credentials(HTTP_AUTHORIZATION="Bearer %s" % access_token)
        response = self.api_client.get(reverse("user_detail"))
        self.assertEqual(response.status_code, 200)
        self.api_client.credentials()
