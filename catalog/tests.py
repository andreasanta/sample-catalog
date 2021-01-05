from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient

from .models import Product

class CatalogTest(TestCase):

    def test_db_insert_product(self):
        Product.objects.create(sku='TEST1', name='Product 1', qty=5, price=1.2)
        product = Product.objects.get(sku='TEST1')

        self.assertIsNotNone(product, 'Product could not be inserted properly')

        self.assertEqual(product.name, 'Product 1')
        self.assertEqual(product.qty, 5)
        self.assertAlmostEquals(product.price, 1.2)


    def test_db_negative_quantity(self):
        self.assertRaises(IntegrityError, Product.objects.create, sku='TEST2', name='Product 2', qty=-2, price=1.2)


    def test_db_negative_price(self):

        p = Product(sku='TEST3', name='Product 3', qty=1, price=-1.2)
        self.assertRaises(ValidationError, p.full_clean)

    
    def test_api_product_basic_insertion_retrieval(self):
        c = APIClient()
        
        insert = c.post('/api/products/', {
            'sku': 'API1',
            'name': 'Api Test 1',
            'price': 15.50,
            'qty': 5
        },  format='json')

        self.assertEqual(insert.status_code, 201)

        product = c.get('/api/products/API1/', format='json')

        self.assertEqual(insert.status_code, 201)

        # Assert timestamps, then pop and compare
        self.assertIsNotNone(product.data.get('created_at'))
        self.assertIsNotNone(product.data.get('updated_at'))

        product.data.pop('created_at')
        product.data.pop('updated_at')

        self.assertDictEqual(product.data, {
            'sku': 'API1',
            'name': 'Api Test 1',
            'price': 15.50,
            'qty': 5
        })

    def test_api_product_basic_available_items(self):
        c = APIClient()
        
        c.post('/api/products/', {
            'sku': 'API2',
            'name': 'Api Test 2',
            'price': 15.50,
            'qty': 5
        },  format='json')

        product = c.get('/api/products/?stock=available')

        self.assertEqual(product.status_code, 200)
        self.assertGreater(len(product.data), 0)


    def test_api_product_basic_unavailable_items(self):
        c = APIClient()
        
        c.post('/api/products/', {
            'sku': 'API3',
            'name': 'Api Test 3',
            'price': 15.50,
            'qty': 0
        },  format='json')

        product = c.get('/api/products/?stock=notavailable')

        self.assertEqual(product.status_code, 200)
        self.assertGreater(len(product.data), 0)

    def test_api_product_valid_quantity_update(self):
        c = APIClient()

        insert = c.post('/api/products/', {
            'sku': 'API4',
            'name': 'Api Test 4',
            'price': 15.50,
            'qty': 5
        },  format='json')
        
        insert = c.patch('/api/products/API4/', {
            'qty': -1
        },  format='json')

        self.assertEqual(insert.status_code, 200)

        product = c.get('/api/products/API4/', format='json')

        self.assertEqual(product.status_code, 200)

        # Assert timestamps, then pop and compare
        self.assertIsNotNone(product.data.get('created_at'))
        self.assertIsNotNone(product.data.get('updated_at'))

        product.data.pop('created_at')
        product.data.pop('updated_at')

        self.assertDictEqual(product.data, {
            'sku': 'API4',
            'name': 'Api Test 4',
            'price': 15.50,
            'qty': 4
        })

    def test_api_product_invalid_quantity_update(self):
        c = APIClient()

        c.post('/api/products/', {
            'sku': 'API5',
            'name': 'Api Test 5',
            'price': 15.50,
            'qty': 5
        },  format='json')
        
        patch = c.patch('/api/products/API5/', {
            'qty': -6
        },  format='json')

        self.assertEqual(patch.status_code, 400)

        product = c.get('/api/products/API5/', format='json')

        self.assertEqual(product.status_code, 200)

        # Assert timestamps, then pop and compare
        self.assertIsNotNone(product.data.get('created_at'))
        self.assertIsNotNone(product.data.get('updated_at'))

        product.data.pop('created_at')
        product.data.pop('updated_at')

        self.assertDictEqual(product.data, {
            'sku': 'API5',
            'name': 'Api Test 5',
            'price': 15.50,
            'qty': 5
        })