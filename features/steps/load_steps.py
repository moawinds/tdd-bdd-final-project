import requests
from behave import given

@given('the following products')
def step_impl(context):
    """Delete all Products and load new ones"""
    rest_endpoint = f"{context.BASE_URL}/products"
    context.resp = requests.get(rest_endpoint)
    for product in context.resp.json():
        requests.delete(f"{rest_endpoint}/{product['id']}")
    
    for row in context.table:
        payload = {
            "name": row['name'],
            "description": "BDD Test Data",
            "price": "10.00",
            "available": row['available'] in ['True', 'true', '1'],
            "category": row['category']
        }
        requests.post(rest_endpoint, json=payload)    # List all of the products and delete them one by one
    #
    rest_endpoint = f"{context.base_url}/products"
    context.resp = requests.get(rest_endpoint)
    assert(context.resp.status_code == HTTP_200_OK)
    for product in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{product['id']}")
        assert(context.resp.status_code == HTTP_204_NO_CONTENT)

    #
    # load the database with new products
    #
    for row in context.table:
        #
        # ADD YOUR CODE HERE TO CREATE PRODUCTS VIA THE REST API
        #
