from flask import render_template, session, request, redirect, url_for, flash
from shop import app, db, photos
from .models import Brand, Category
from .forms import Addproducts

@app.route("/addbrand", methods=['GET','POST'])
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
def add_category():
    if request.method == "POST":
        get_category = request.form.get("category")
        category = Category(name=get_category)
        db.session.add(category)
        flash(f'The category {get_category} was added to your database',"success")
        db.session.commit()
        return redirect(url_for("add_category"))

    return render_template("products/addcategory.html", categories="categories")

@app.route("/updatebrand/<int:id>", methods=['GET','POST'])
def update_brand(id):
    if "email" not in session:
        flash(f"Please login first", "danger")
    update_brand = Brand.query.get_or_404(id)
    brand = request.form.get("brand")
    if request.method == "POST":
        update_brand.name = brand
        flash(f"Your brand has been updated","success")
        db.session.commit()
        return redirect(url_for("add_brand"))

    return render_template("products/updatebrand.html", updatebrands="updatebrands")

@app.route("/updatecategory/<int:id>", methods=['GET','POST'])
def update_category(id):
    if "email" not in session:
        flash(f"Please login first", "danger")
    update_category = Category.query.get_or_404(id)
    category = request.form.get("category")
    if request.method == "POST":
        update_category.name = category
        flash(f"Your category has been updated","success")
        db.session.commit()
        return redirect(url_for("add_category"))

    return render_template("products/updatecategory.html", updatecategories="updatecategories")

@app.route("/addproduct", methods=["POST", "GET"])
def add_product():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == "POST":
        photos.save(request.files.get("image_1"))
        photos.save(request.files.get("image_2"))
        photos.save(request.files.get("image_3"))
    return render_template("products/addproduct.html", form=form, brands=brands, categories=categories)