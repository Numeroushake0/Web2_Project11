import unittest
from app.models.contact import Contact


class TestContactModel(unittest.TestCase):
    def setUp(self):
        self.contact = Contact(
            name="John Doe",
            email="john@example.com",
            phone="123456789",
            birthday="1990-01-01",
            user_id=1
        )

    def test_contact_name(self):
        self.assertEqual(self.contact.name, "John Doe")

    def test_contact_email(self):
        self.assertEqual(self.contact.email, "john@example.com")

    def test_contact_phone(self):
        self.assertEqual(self.contact.phone, "123456789")

    def test_contact_user_id(self):
        self.assertEqual(self.contact.user_id, 1)
