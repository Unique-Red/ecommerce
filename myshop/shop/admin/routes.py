from flask import render_template, session, request, redirect, url_for, flash

from shop import app, db # bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from shop.products.models import Addproduct, Brand, Category
import os

@app.route("/")
@app.route("/admin")
@login_required
def admin():
    if 'email' not in session:
        flash("Please login first","danger")
        return redirect(url_for("login"))
    products = Addproduct.query.all()
    return render_template("admin/admin.html", products=products)

@app.route('/brands', methods=['GET', 'POST'])
@login_required
def brands():
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brands.html', brands=brands)

@app.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/categories.html', categories=categories)
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('admin'))
            else:
                flash("Password is incorrect", "danger") 
        else:
            flash("Email does not exist", "danger")

    return render_template ("admin/login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if username_exists:
            flash("Username in use.", "danger")
        if email_exists:
            flash("Email in use.", "danger")
        elif len(username) < 2:
            flash("Username is too short", "danger") 
        elif len(password) < 6:
            flash("Password is too short", "danger")
        else:
            new_user = User(name=name, username=username, email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('admin'))

    return render_template ("admin/register.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/admin")
"""@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.username.data}.Thanks for registering','success')
        return redirect(url_for('admin'))
    return render_template('admin/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {form.email.data}.You are logged in now','success')
            return redirect(url_for('admin'))
        else:
            flash("Wrong password, please try again", "danger")

    return render_template('admin/login.html', form=form)"""

"""
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/home")"""