from flask import jsonify, request, abort
from service.models import Product
from service.common import status  # HTTP Status Codes
from . import app

@app.route("/products", methods=["GET"])
def list_products():
    """Mengembalikan daftar semua produk atau mencari berdasarkan kriteria"""
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        products = Product.find_by_name(name)
    elif category:
        products = Product.find_by_category(category)
    elif available:
        products = Product.find_by_availability(available.lower() in ["true", "1"])
    else:
        products = Product.all()

    results = [product.serialize() for product in products]
    return jsonify(results), status.HTTP_200_OK

@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """Membaca satu produk berdasarkan ID"""
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' not found")
    return jsonify(product.serialize()), status.HTTP_200_OK

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """Memperbarui produk yang sudah ada"""
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' not found")
    
    product.deserialize(request.get_json())
    product.id = product_id
    product.update()
    return jsonify(product.serialize()), status.HTTP_200_OK

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """Menghapus produk"""
    product = Product.find(product_id)
    if product:
        product.delete()
    return "", status.HTTP_204_NO_CONTENT
