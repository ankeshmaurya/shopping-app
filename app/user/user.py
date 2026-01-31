
from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from functools import wraps

user = Blueprint('user', __name__)

# Dummy product data
products_db = {
    1: {'id': 1, 'name': 'Classic Leather Boots', 'category_id': 1, 'price': 150.00},
    2: {'id': 2, 'name': 'Winter Wool Coat', 'category_id': 2, 'price': 250.00},
    3: {'id': 3, 'name': 'Denim Jacket', 'category_id': 3, 'price': 90.00},
    4: {'id': 4, 'name': 'Baseball Cap', 'category_id': 4, 'price': 25.00},
    5: {'id': 5, 'name': 'Running Sneakers', 'category_id': 5, 'price': 120.00},
    6: {'id': 6, 'name': 'Smartwatch', 'category_id': 6, 'price': 300.00}
}
categories_db = {
    1: 'Boots',
    2: 'Coats',
    3: 'Jackets',
    4: 'Caps',
    5: 'Footwear',
    6: 'Electronics'
}

# In-memory cart storage
carts = {}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'user':
            flash('You must be logged in as a user to view this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@user.route('/products')
def product_catalog():
    """Displays the product catalog."""
    return render_template('products.html', products=products_db, categories=categories_db)

@user.route('/cart')
@login_required
def view_cart():
    """Displays the user's shopping cart."""
    user_id = session['user_id']
    user_cart = carts.get(user_id, {})
    cart_items = {pid: {'product': products_db[pid], 'quantity': qty} for pid, qty in user_cart.items()}
    total_price = sum(item['product']['price'] * item['quantity'] for item in cart_items.values())
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@user.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """Adds a product to the user's cart."""
    user_id = session['user_id']
    if user_id not in carts:
        carts[user_id] = {}
    
    quantity = int(request.form.get('quantity', 1))
    carts[user_id][product_id] = carts[user_id].get(product_id, 0) + quantity
    flash(f'{products_db[product_id]["name"]} added to cart.', 'success')
    return redirect(url_for('user.product_catalog'))

@user.route('/remove_from_cart/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    """Removes an item from the cart."""
    user_id = session['user_id']
    if user_id in carts and product_id in carts[user_id]:
        del carts[user_id][product_id]
        flash('Item removed from cart.', 'success')
    return redirect(url_for('user.view_cart'))

@user.route('/update_cart/<int:product_id>', methods=['POST'])
@login_required
def update_cart(product_id):
    """Updates the quantity of an item in the cart."""
    user_id = session['user_id']
    quantity = int(request.form['quantity'])
    if user_id in carts and product_id in carts[user_id]:
        if quantity > 0:
            carts[user_id][product_id] = quantity
            flash('Cart updated.', 'success')
        else:
            del carts[user_id][product_id]
            flash('Item removed from cart.', 'success')
    return redirect(url_for('user.view_cart'))

@user.route('/checkout')
@login_required
def checkout():
    """Displays the checkout page with payment options."""
    user_id = session['user_id']
    user_cart = carts.get(user_id, {})
    total_price = sum(products_db[pid]['price'] * qty for pid, qty in user_cart.items())
    return render_template('checkout.html', total_price=total_price)

@user.route('/payment', methods=['POST'])
@login_required
def process_payment():
    """Simulates payment processing."""
    payment_method = request.form['payment_method']
    user_id = session['user_id']
    user_cart = carts.get(user_id, {})
    total_price = sum(products_db[pid]['price'] * qty for pid, qty in user_cart.items())

    # Clear cart after checkout
    carts[user_id] = {}

    flash(f'You will be redirected to {payment_method} to pay \u20b9{total_price}', 'info')
    flash('Your order is successfully placed!', 'success')
    return redirect(url_for('user.product_catalog'))
