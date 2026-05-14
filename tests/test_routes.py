from unittest import TestCase
from service import app
from service.models import db, Product
from tests.factories import ProductFactory
from service.common import status

BASE_URL = "/products"

class TestProductRoutes(TestCase):
    """Product Service Rest Api Tests"""

    @classmethod
    def setUpClass(cls):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        Product.init_db(app)

    def setUp(self):
        db.session.query(Product).delete()
        db.session.commit()
        self.client = app.test_client()

    def test_get_product(self):
        """It should Get a single Product"""
        test_product = ProductFactory()
        test_product.create()
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json()["name"], test_product.name)

    def test_update_product(self):
        """It should Update an existing Product"""
        test_product = ProductFactory()
        test_product.create()
        new_product = test_product.serialize()
        new_product["name"] = "New Name"
        response = self.client.put(f"{BASE_URL}/{test_product.id}", json=new_product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json()["name"], "New Name")

    def test_delete_product(self):
        """It should Delete a Product"""
        test_product = ProductFactory()
        test_product.create()
        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_product_list(self):
        """It should Get a list of Products"""
        for _ in range(5):
            ProductFactory().create()
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.get_json()), 5)
