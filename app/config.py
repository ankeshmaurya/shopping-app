
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-secret-key'

products_db = {
    1: {'name': 'T-shirt', 'category_id': 1, 'price': 500, 'image': '/static/uploads/t-shirt.jpg'},
    2: {'name': 'Jeans', 'category_id': 1, 'price': 1500, 'image': '/static/uploads/jeans.jpg'},
    3: {'name': 'Laptop', 'category_id': 2, 'price': 50000, 'image': '/static/uploads/laptop.jpg'},
    4: {'name': 'Mobile', 'category_id': 2, 'price': 20000, 'image': '/static/uploads/mobile.jpg'},
    5: {'name': 'Belt', 'category_id': 1, 'price': 300, 'image': '/static/uploads/belt.jpg'}
}

categories_db = {
    1: 'Clothing',
    2: 'Electronics'
}
