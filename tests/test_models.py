from unittest import TestCase
from service.models import Product, db
from tests.factories import ProductFactory
from service import app

class TestProductModel(TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        Product.init_db(app)

    def setUp(self):
        db.session.query(Product).delete()
        db.session.commit()

    def test_read_a_product(self):
        """It should Read a Product"""
        product = ProductFactory()
        product.create()
        found_product = Product.find(product.id)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)

    def test_update_a_product(self):
        """It should Update a Product"""
        product = ProductFactory()
        product.create()
        product.name = "Updated Name"
        product.update()
        self.assertEqual(product.name, "Updated Name")

    def test_delete_a_product(self):
        """It should Delete a Product"""
        product = ProductFactory()
        product.create()
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_list_all_products(self):
        """It should List all Products"""
        for _ in range(5):
            ProductFactory().create()
        self.assertEqual(len(Product.all()), 5)
