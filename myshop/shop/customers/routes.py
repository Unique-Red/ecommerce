from flask import render_template, session, request, redirect, url_for, flash, current_app
from shop import app, db, products, search
from .forms import CustomerRegistrationForm, CustomerLoginForm
from .models import Register
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import os


@app.route("/customer/register", methods=["GET", "POST"])
def customer_register():
    form = CustomerRegistrationForm(request.form)
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        country = request.form.get("country")
        state = request.form.get("state")
        city = request.form.get("city")
        contact = request.form.get("contact")
        address = request.form.get("address")
        
        email_exists = Register.query.filter_by(email=email).first()
        username_exists = Register.query.filter_by(username=username).first()
        if username_exists:
            flash("Username in use.", "danger")
        if email_exists:
            flash("Email in use.", "danger")
        elif len(username) < 2:
            flash("Username is too short", "danger") 
        elif len(password) < 6:
            flash("Password is too short", "danger")
        else:
            new_customer = Register(name=name, username=username, email=email, password=generate_password_hash(password, method='sha256'), country=country, state=state, city=city, contact=contact, address=address)
            db.session.add(new_customer)
            flash(f'Welcome {name}. Thank you for registering', "success")
            db.session.commit()

            return redirect(url_for('home'))

    return render_template ("customer/register.html", form=form)

@app.route("/customer/login", methods=["GET", "POST"])
def customer_login():
    form = CustomerLoginForm(request.form)
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = Register.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                flash("Password is incorrect", "danger") 
        else:
            flash("Email does not exist", "danger")

    return render_template ("customer/login.html", form=form)

@app.route("/customer/logout")
def customer_logout():
    logout_user()
    return redirect(url_for("home"))