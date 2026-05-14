import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Inisialisasi SQLAlchemy
db = SQLAlchemy()

class DataValidationError(Exception):
    """Digunakan untuk kesalahan validasi data dari deserialisasi"""

class Category:
    """Enumerasi Kategori Produk"""
    UNKNOWN = "UNKNOWN"
    CLOTHS = "CLOTHS"
    FOOD = "FOOD"
    ELECTRONICS = "ELECTRONICS"
    FURNITURE = "FURNITURE"

class Product(db.Model):
    """
    Kelas yang merepresentasikan sebuah Produk
    """
    app = None

    # Tabel Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    description = db.Column(db.String(256))
    price = db.Column(db.Decimal(10, 2), nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=True)
    category = db.Column(db.String(63), nullable=False, server_default=Category.UNKNOWN)

    def __repr__(self):
        return f"<Product {self.name} id=[{self.id}]>"

    def create(self):
        """Membuat produk baru ke database"""
        logger.info("Creating %s", self.name)
        self.id = None  # id harus None agar database bisa menentukannya
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Memperbarui produk yang sudah ada"""
        logger.info("Updating %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """Menghapus produk dari database"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Mengubah objek menjadi dictionary untuk JSON"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "available": self.available,
            "category": self.category
        }

    def deserialize(self, data):
        """Mengubah dictionary menjadi objek Produk"""
        try:
            self.name = data["name"]
            self.description = data.get("description")
            self.price = data["price"]
            self.available = data["available"]
            self.category = data["category"]
        except KeyError as error:
            raise DataValidationError("Invalid Product: missing " + error.args
