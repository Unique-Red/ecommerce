from flask import render_template, session, request, redirect, url_for, flash, current_app
from shop import app, db, products, search
from flask_login import login_required
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import os

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def brands():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return brands

def categories():
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return categories


@app.route("/")
def home():
    page = request.args.get("page", 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).order_by(Addproduct.id.desc()). paginate(page=page, per_page=8)
    return render_template("products/product.html", products=products, brands=brands(), categories=categories())

@app.route("/result")
def result():
    searchword = request.args.get('q')
    products = Addproduct.query.msearch(searchword, fields=['name','description'], limit=4)
    return render_template("products/result.html",products=products, brands=brands(), categories=categories())

@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    return render_template("products/singlepage.html", product=product, brands=brands(), categories=categories())


@app.route("/brand/<int:id>")
def get_brand(id):
    page = request.args.get("page", 1, type=int)
    get_b = Brand.query.filter_by(id=id).first_or_404()
    brand = Addproduct.query.filter_by(brand=get_b). paginate(page=page, per_page=4)
    return render_template("products/brands.html", brand=brand, brands=brands(), categories=categories(), get_b=get_b)

@app.route("/categories/<int:id>")
def get_category(id):
    page = request.args.get("page", 1, type=int)
    get_c = Category.query.filter_by(id=id).first_or_404()
    get_category_product = Addproduct.query.filter_by(category=get_c).paginate(page=page, per_page=4)
    return render_template('products/category.html', get_category_product=get_category_product, categories=categories(), brands=brands(), get_c=get_c)

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
        product.brand_id = brand
        product.category_id = category
        product.stock = form.stock.data
        product.colours = form.colours.data
        product.description = form.description.data
        
        image_1 = request.files.get("image_1")
        path1 = os.path.join("shop", "static", "uploads", image_1.filename)
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/uploads/" + product.image_1))
                image_1.save(path1)
                product.image_1 = os.path.join("shop", "static", "uploads", image_1.filename)
            except:
                
                path1 = os.path.join("shop", "static", "uploads", image_1.filename)

        image_2 = request.files.get("image_2")
        path2 = os.path.join("shop", "static", "uploads", image_2.filename)
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/uploads/" + product.image_2))
                image_2.save(path2)
                product.image_2 = os.path.join("shop", "static", "uploads", image_2.filename)
            except:            
                path2 = os.path.join("shop", "static", "uploads", image_2.filename)

        image_3 = request.files.get("image_3")
        path3 = os.path.join("shop", "static", "uploads", image_3.filename)
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/uploads/" + product.image_3))
                image_3.save(path3)
                product.image_1 = os.path.join("shop", "static", "uploads", image_3.filename)
            except:
                    
                path3 = os.path.join("shop", "static", "uploads", image_3.filename)

        db.session.commit()
        flash("Product updated", "success")
        return redirect(url_for("admin"))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colours.data = product.colours
    form.description.data = product.description

    return render_template("products/updateproduct.html", form=form, brands=brands, categories=categories, product=product)

@app.route("/deletebrand/<int:id>", methods=["POST"])
@login_required
def delete_brand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(brand)
        db.session.commit()
        flash(f"The brand {brand.name} was deleted from your database", "success")
        return redirect(url_for("brands"))
    else:
        flash("There was a problem deleting this brand", "warning")
        return redirect(url_for("admin"))


@app.route("/deletecategory/<int:id>", methods=["POST"])
@login_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(category)
        db.session.commit()
        flash(f"The category {category.name} was deleted from your database", "success")
        return redirect(url_for("categories"))
    else:
        flash("There was a problem deleting this category", "warning")
        return redirect(url_for("admin"))

@app.route("/deleteproduct/<int:id>", methods=["POST"])
@login_required
def delete_product(id):
    product = Addproduct.query.get_or_404(id)
    if request.method == "POST":
        if request.files.get('image_1', 'image_2', 'image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/uploads/" + product.image_1))
                os.unlink(os.path.join(current_app.root_path, "static/uploads/" + product.image_2))
                os.unlink(os.path.join(current_app.root_path, "static/uploads/" + product.image_3))
            except Exception  as e:
                print(e)

        db.session.delete(product)
        db.session.commit()
        flash(f"The product {product.name} was deleted from your database", "success")
        return redirect(url_for("admin"))
    else:
        flash("There was a problem deleting this product", "warning")
        return redirect(url_for("admin"))