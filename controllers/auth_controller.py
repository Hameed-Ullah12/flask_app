from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user,logout_user,login_required,current_user

from models.user_model import User
from forms.auth_forms import RegisterForm, LoginForm
from extensions import db


auth = Blueprint("auth", __name__)


@auth.route("/")
def home():
    return render_template("home.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            username=form.username.data,
            email=form.email.data
        )

        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)

            if user.role == "admin":
                return redirect(url_for("auth.admin_dashboard"))

            return redirect(url_for("auth.dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)


@auth.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@auth.route("/admin")
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        flash("Unauthorized", "danger")
        return redirect(url_for("auth.dashboard.html"))

    return render_template("admin_dashboard.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.home"))
