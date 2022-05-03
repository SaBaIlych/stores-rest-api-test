from models.store import StoreModel
from models.item import ItemModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel('test')

        self.assertListEqual(store.items.all(), [],
                                    "The store items is not equal to the empty list")


    def test_crud(self):
        with self.app_context():    
            store = StoreModel('test')

            self.assertIsNone(StoreModel.find_by_name('test'), "Found a store with name 'test' even though it wasn't written to the database")

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('test'), "Didn't found a store with name 'test even though it was written in database")

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('test'), "Found a store with name 'test' even though it was delete from the database")


    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test item', 100, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'test item')


    def test_store_json_no_items(self):
        store = StoreModel('test')
    
        expected = {
            'name': 'test',
            'items': []
        }

        self.assertDictEqual(store.json(), expected)


    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test item', 100, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {
                'name': 'test',
                'items': [
                    {
                        'name': 'test item',
                        'price': 100
                    }

                ]
            }

            self.assertDictEqual(store.json(), expected)
    