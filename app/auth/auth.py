
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth = Blueprint('auth', __name__)

# Dummy databases
users_db = {'user': {'password': 'user', 'user_id': 1}}
admins_db = {'admin': {'password': 'admin'}}

@auth.route('/')
def welcome():
    """Renders the welcome screen with login options."""
    return render_template('welcome.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handles both user and admin login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login_type = request.form['login_type']

        if login_type == 'user':
            if username in users_db and users_db[username]['password'] == password:
                session['user_id'] = users_db[username]['user_id']
                session['role'] = 'user'
                return redirect(url_for('user.product_catalog'))
            else:
                flash('Invalid user credentials!', 'danger')
        elif login_type == 'admin':
            if username in admins_db and admins_db[username]['password'] == password:
                session['user_id'] = username
                session['role'] = 'admin'
                return redirect(url_for('admin.dashboard'))
            else:
                flash('Invalid admin credentials!', 'danger')
        
        return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth.route('/logout')
def logout():
    """Clears the session and redirects to the welcome page."""
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.welcome'))
