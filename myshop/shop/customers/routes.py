from typing import OrderedDict
from flask import render_template, session, request, redirect, url_for, flash, current_app, make_response
from werkzeug.datastructures import RequestCacheControl
from werkzeug.wrappers import response
from shop import app, db, products, search
from .forms import CustomerRegistrationForm, CustomerLoginForm
from .models import Register, CustomerOrder
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
import pdfkit


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

@app.route("/getorder")
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash("Your order has been sent successfully", "success")
            return redirect(url_for("orders", invoice=invoice))
        except Exception as e:
            print(e)
            flash("Something went wrong while getting order","danger")
            return redirect(url_for('getCart'))

@app.route('/orders/<invoice>')
def orders(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
        for _key, product in orders.orders.items():
            discount = (product['discount']/100 * float(product['price']))
            subTotal += float(product['price']) * int(product['quantity'])
            subTotal -= discount
            tax = ("%.2f" % (.06 * float(subTotal)))
            grandTotal = float("%.2f" % (1.06 * subTotal))
    else:
        return redirect(url_for('customer_login'))
    return render_template("customer/order.html", invoice=invoice, tax=tax, subTotal=subTotal, grandTotal=grandTotal, customer=customer, orders=orders)

@app.route('/get_pdf/<invoice>', methods=['POST'])
def get_pdf(invoice):
    if current_user.is_authenticated:
        grandTotal = 0
        subTotal = 0
        customer_id = current_user.id
        if request.method == "POST":
            customer = Register.query.filter_by(id=customer_id).first()
            orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
            for _key, product in orders.orders.items():
                discount = (product['discount']/100 * float(product['price']))
                subTotal += float(product['price']) * int(product['quantity'])
                subTotal -= discount
                tax = ("%.2f" % (.06 * float(subTotal)))
                grandTotal = float("%.2f" % (1.06 * subTotal))


            rendered = render_template("customer/pdf.html", invoice=invoice, tax=tax, grandTotal=grandTotal, customer=customer, orders=orders)
            pdf = pdfkit.from_string(rendered, False)
            response = make_response(pdf)
            response.headers['content-Type']='application/pdf'
            response.headers['content-Disposition']='inline: filename='+invoice+'.pdf'
            return response

    return redirect(url_for('orders'))