import os

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    current_app
)

from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.product_model import Product
from forms.product_forms import ProductForm
from extensions import db


product = Blueprint("product", __name__)

# VIEW PRODUCTS
@product.route("/products")
@login_required
def view_products():

    products = Product.query.all()
    return render_template("products.html", products=products)


# ADD PRODUCT
@product.route("/products/add", methods=["GET", "POST"])
@login_required
def add_product():

    if current_user.role !="admin":
        flash("Unauthorized Access")
        return redirect(url_for("auth.dashboard"))

    form = ProductForm()

    if form.validate_on_submit():

        image_file = None

        if form.image.data:
            filename = secure_filename(form.image.data.filename)

            image_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"], filename
            )

            form.image.data.save(image_path)
            image_file = filename
                

        product_data = Product(
            title=form.title.data,
            description=form.description.data,
            quantity=form.quantity.data,
            image=image_file,
        )

        db.session.add(product_data)
        db.session.commit()

        flash("Product added successfully.")

        return redirect(url_for("product.view_products"))

    return render_template("add_product.html", form=form)


# EDIT PRODUCT
@product.route("/edit-product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):

    if current_user.role !="admin":
        flash("Unauthorized Access")
        return redirect(url_for("auth.dashboard"))


    product = Product.query.filter_by(id=product_id)

    form = ProductForm(obj=product_id)

    if form.validate_on_submit():

        product.title = form.title.data
        product.description = form.description.data
        product.quantity = form.quantity.data

        if form.image.data:

            filename = secure_filename(form.image.data.filename)

            image_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"],filename
            )


            form.image.data.save(image_path)
            

            product_data.image = filename

        db.session.commit()

        flash("Product updated successfully!")

        return redirect(url_for("product.view_products"))

    return render_template(
        "edit_product.html",
        form=form,
        product=product
    )


# DELETE PRODUCT
@product.route("/delete-product/<int:product_id>")
@login_required
def delete_product(product_id):

    if current_user.role !="admin":
        flash("Unauthorized Access")
        return redirect(url_for("auth.dashboard"))

    product = Product.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    flash("Product deleted successfully!")

    return redirect(url_for("product.view_products"))
