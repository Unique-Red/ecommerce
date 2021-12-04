from itertools import product
from sys import path
from flask import render_template, session, request, redirect, url_for, flash
from shop import app, db #,photos
from flask_login import login_required
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import os

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


@app.route("/addbrand", methods=['GET','POST'])
@login_required
def add_brand():
    if request.method == "POST":
        get_brand = request.form.get("brand")
        brand = Brand(name=get_brand)

        db.session.add(brand)
        flash(f'The brand {get_brand} was added to your database',"success")
        db.session.commit()
        return redirect(url_for("add_brand"))

    return render_template("products/addbrand.html", brands="brands")

@app.route("/addcategory", methods=['GET','POST'])
@login_required
def add_category():
    if 'email' not in session:
        flash("Please login first","danger")
        return redirect(url_for("login"))
    if request.method == "POST":
        get_category = request.form.get("category")
        category = Category(name=get_category)
        db.session.add(category)
        flash(f'The category {get_category} was added to your database',"success")
        db.session.commit()
        return redirect(url_for("add_category"))

    return render_template("products/addcategory.html", categories="categories")

@app.route("/updatebrand/<int:id>", methods=['GET','POST'])
@login_required
def update_brand(id):
    update_brand = Brand.query.get_or_404(id)
    brand = request.form.get("brand")
    if request.method == "POST":
        update_brand.name = brand
        flash(f"Your brand has been updated","success")
        db.session.commit()
        return redirect(url_for("brands"))

    return render_template("products/updatebrand.html", update_brand=update_brand)

@app.route("/updatecategory/<int:id>", methods=['GET','POST'])
@login_required
def update_category(id):
    update_category = Category.query.get_or_404(id)
    category = request.form.get("category")
    if request.method == "POST":
        update_category.name = category
        flash(f"Your category has been updated","success")
        db.session.commit()
        return redirect(url_for("categories"))

    return render_template("products/updatecategory.html", update_category=update_category)

@app.route("/addproduct", methods=["POST", "GET"])
@login_required
def add_product():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        discount = request.form.get("discount")
        stock = request.form.get("stock")
        colours = request.form.get("colours")
        description = request.form.get("description")
        """name = form.name.data
        price = request.form.get("price")
        discount = form.discount.data
        stock = form.stock.data
        colours = form.colours.data
        description = form.description.data"""
        brand = request.form.get("brand")
        category = request.form.get("category")

        image_1 = request.files.get("image_1")
        image_2 = request.files.get("image_2")
        image_3 = request.files.get("image_3")

        if not image_3:
            flash ("Fill all categories!")
        else:
            path1 = os.path.join("shop", "static", "uploads", image_1.filename)
            path2 = os.path.join("shop", "static", "uploads", image_2.filename)
            path3 = os.path.join("shop", "static", "uploads", image_3.filename)


        print (price)
        add_product = Addproduct(name=name, discount=discount, price=price, stock=stock, colours=colours, description=description, brand_id=brand, category_id=category, image_1=image_1.filename, image_2=image_2.filename, image_3=image_3.filename)
        image_1.save(path1)
        image_2.save(path2)
        image_3.save(path3)
        db.session.add(add_product)
        flash(f"The product {name} has been added to your database", "success")
        db.session.commit()
        return redirect(url_for("add_product"))

    return render_template("products/addproduct.html", form=form, brands=brands, categories=categories)


@app.route("/updateproduct/<int:id>", methods=['GET','POST'])
def update_product(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    form = Addproducts(request.form)
    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.colours = form.colours.data
        product.description = form.description.data
        db.session.commit()
        flash("Product updated", "success")
        return redirect("admin")
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colours.data = product.colours
    form.description.data = product.description

    return render_template("products/updateproduct.html", form=form, brands=brands, categories=categories, product=product)