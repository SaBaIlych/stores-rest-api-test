from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client: # we're going to be making requests to our API test client, so we need a client
            with self.app_context(): # cause we use database to save records we need app context
                response = client.post('/register', json={'username': 'test', 'password': '1234'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User created successfully.'},
                                        json.loads(response.data))
            

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', json={'username': 'test', 'password': '1234'})
                auth_response = client.post('/auth',
                                             json={'username': 'test', 'password': '1234'},
                                            headers = {'Content-Type': 'application/json'})
                
                self.assertIn('access_token', json.loads(auth_response.data).keys())


    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', json={'username': 'test', 'password': '1234'})
                response = client.post('/register', json={'username': 'test', 'password': '1234'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with that username already exist'}, json.loads(response.data))