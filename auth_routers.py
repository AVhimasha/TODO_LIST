from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from model import db, User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('task.index'))
        flash("Invalid credentials.")
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        if User.query.filter_by(username=username).first():
            flash("Username already exists. Please choose a different one.")
            return redirect(url_for('auth.register'))
        hashed_pw = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        user = User(username=username, password=hashed_pw)  # type: ignore
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.")
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        username = request.form.get('username')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        
        # Check if username is being changed and if it already exists
        if username != current_user.username:
            if User.query.filter_by(username=username).first():
                flash("Username already exists. Please choose a different one.")
                return redirect(url_for('auth.profile'))
        
        # Verify current password if changing password
        if new_password:
            if not current_password or not check_password_hash(current_user.password, current_password):
                flash("Current password is incorrect.")
                return redirect(url_for('auth.profile'))
            
            # Update password
            current_user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
        
        # Update username
        current_user.username = username
        db.session.commit()
        flash("Profile updated successfully!")
        return redirect(url_for('auth.profile'))
    
    return render_template('profile.html')
