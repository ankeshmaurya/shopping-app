
from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from functools import wraps
from app.config import products_db, categories_db
import os
from werkzeug.utils import secure_filename

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('You must be logged in as an admin to view this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/')
@admin_required
def dashboard():
    """Displays the admin dashboard with all products and categories."""
    return render_template('admin/dashboard.html', products=products_db, categories=categories_db)

@admin.route('/add_product', methods=['POST'])
@admin_required
def add_product():
    """Adds a new product to the catalog."""
    name = request.form['name']
    category_id = int(request.form['category_id'])
    price = float(request.form['price'])
    
    image = request.files['image']
    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join('app', 'static', 'uploads', filename)
        image.save(image_path)
        image_url = f'/static/uploads/{filename}'
    else:
        image_url = None

    new_product_id = max(products_db.keys()) + 1
    products_db[new_product_id] = {'name': name, 'category_id': category_id, 'price': price, 'image': image_url}
    
    flash(f'Product "{name}" added successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/update_product/<int:product_id>', methods=['POST'])
@admin_required
def update_product(product_id):
    """Updates an existing product."""
    name = request.form['name']
    category_id = int(request.form['category_id'])
    price = float(request.form['price'])
    
    image = request.files.get('image')
    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join('app', 'static', 'uploads', filename)
        image.save(image_path)
        image_url = f'/static/uploads/{filename}'
    else:
        image_url = products_db[product_id]['image']

    if product_id in products_db:
        products_db[product_id] = {'name': name, 'category_id': category_id, 'price': price, 'image': image_url}
        flash(f'Product ID {product_id} updated successfully!', 'success')
    else:
        flash('Product not found!', 'danger')
    
    return redirect(url_for('admin.dashboard'))

@admin.route('/delete_product/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    """Deletes a product from the catalog."""
    if product_id in products_db:
        # Delete the image file if it exists
        image_path = products_db[product_id].get('image')
        if image_path and os.path.exists(image_path.replace('/static', 'app/static', 1)):
            os.remove(image_path.replace('/static', 'app/static', 1))

        del products_db[product_id]
        flash(f'Product ID {product_id} deleted successfully!', 'success')
    else:
        flash('Product not found!', 'danger')
    
    return redirect(url_for('admin.dashboard'))

@admin.route('/add_category', methods=['POST'])
@admin_required
def add_category():
    """Adds a new product category."""
    name = request.form['name']
    new_category_id = max(categories_db.keys()) + 1
    categories_db[new_category_id] = name
    
    flash(f'Category "{name}" added successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/delete_category/<int:category_id>', methods=['POST'])
@admin_required
def delete_category(category_id):
    """Deletes a product category."""
    if category_id in categories_db:
        # Optional: Check if any product is using this category before deleting
        if any(p['category_id'] == category_id for p in products_db.values()):
            flash(f'Cannot delete category "{categories_db[category_id]}" as it is in use.', 'danger')
        else:
            del categories_db[category_id]
            flash(f'Category ID {category_id} deleted successfully!', 'success')
    else:
        flash('Category not found!', 'danger')
        
    return redirect(url_for('admin.dashboard'))
