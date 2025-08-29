import unittest
from app.models.user import User


class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.user = User(
            username="testuser",
            email="test@example.com",
            hashed_password="hashedpassword123"
        )

    def test_user_username(self):
        self.assertEqual(self.user.username, "testuser")

    def test_user_email(self):
        self.assertEqual(self.user.email, "test@example.com")

    def test_user_password(self):
        self.assertEqual(self.user.hashed_password, "hashedpassword123")
