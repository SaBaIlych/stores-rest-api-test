from tests.base_test import BaseTest
from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth',
                                json={'username': 'test', 'password': '1234'},
                                headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'


    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')

                self.assertEqual(resp.status_code, 401)


    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test', headers = {'Authorization': self.access_token})

                self.assertEqual(resp.status_code, 404)


    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 100, 1).save_to_db()
                resp = client.get('/item/test', headers = {'Authorization': self.access_token})

                self.assertEqual(resp.status_code, 200)


    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 100, 1).save_to_db()
                resp = client.delete('/item/test')

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(json.loads(resp.data), {'message': 'Item deleted'})


    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.post('/item/test', json={'price': 100, 'store_id': 1})

                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual(json.loads(resp.data), {'name': 'test', 'price': 100})


    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                client.post('/item/test', json={'price': 100, 'store_id': 1})
                resp = client.post('/item/test', json={'price': 100, 'store_id': 1})

                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual(json.loads(resp.data), {'message': "An item with name 'test' already exists."})


    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.put('/item/test', json={'price': 100, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 100)
                self.assertDictEqual(json.loads(resp.data), {'name': 'test', 'price': 100})


    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 100, 1).save_to_db()

                self.assertEqual(ItemModel.find_by_name('test').price, 100)
                resp = client.put('/item/test', json={'price': 50, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 50)
                self.assertDictEqual(json.loads(resp.data), {'name': 'test', 'price': 50})


    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 100, 1).save_to_db()
                resp = client.get('/items')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'items':[{'name': 'test', 'price': 100}]})