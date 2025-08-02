from django.test import TestCase
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.utils.dateparse import parse_date

class CustomUserDBTest(TestCase):
    # def test_user_creation_and_retrieval(self):
    #     username = 'testuser'
    #     email = "testemail@gmail.com"
    #     password1 = 'TestPassword123!'
    #     dob = '1990-01-01'
    #     gender = 'M'
    #     marital_status = 'Single'
    #     agree_to_terms = True

    #     user = CustomUser.objects.create(
    #         username=username,
    #         email=email,
    #         password=make_password(password1),
    #         dob=parse_date(dob),
    #         gender=gender,
    #         marital_status=marital_status,
    #         agree_to_terms=agree_to_terms
    #     )

    #     # Assert user exists in DB
    #     self.assertTrue(CustomUser.objects.filter(username=username).exists())
    #     # Assert fields are correct
    #     retrieved = CustomUser.objects.get(username=username)
    #     self.assertEqual(retrieved.email, email)
    #     self.assertEqual(retrieved.gender, gender)
    #     self.assertEqual(retrieved.marital_status, marital_status)
    #     self.assertEqual(retrieved.agree_to_terms, agree_to_terms)

    def test_list_all_users(self):
        # Create sample users
        # CustomUser.objects.create(
        #     username='user1',
        #     email='user1@example.com',
        #     password=make_password('pass1')
        # )
        # CustomUser.objects.create(
        #     username='user2',
        #     email='user2@example.com',
        #     password=make_password('pass2')
        # )

        # List all users as dicts
        users_list = list(CustomUser.objects.values())
        print(users_list)  # For demonstration; in real tests, use assertions

        # Assert the list contains the created users
        # self.assertTrue(any(u['username'] == 'user1' for u in users_list))
        # self.assertTrue(any(u['username'] == 'user2' for u in users_list))

