from tests.unit.unit_base_test import UnitBaseTest
from models.user import UserModel


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('test username', 'test password')

        self.assertEqual(user.username, 'test username',
                                                    'The created user name not equal to expected')
        self.assertEqual(user.password, 'test password', 
                                                    'The created user password not equal to expected')
    