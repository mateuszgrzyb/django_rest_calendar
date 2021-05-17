import uuid

from django.test import TestCase
from rest_framework.test import APITestCase


# Create your tests here.
from user.models import User, Manager, Administrator, Participant, Owner


class UserModelTestCase(TestCase):

    def test_role_hook_creation(self):
        roles = [
            'Manager',
            'Owner',
            'Participant',
            'Administrator',
        ]

        for role in roles:
            User.objects.create_user(
                username=f'{role.lower()}1',
                password='1234',
                role_name=role,
                company_id=uuid.uuid4(),
            )

        self.assertEqual(Manager.objects.count(), 1, 'No of manager roles')
        self.assertEqual(Owner.objects.count(), 1, 'No of owner roles')
        self.assertEqual(Participant.objects.count(), 1, 'No of participant roles')
        self.assertEqual(Administrator.objects.count(), 1, 'No of administrator roles')

