"""Contains the auth blueprint."""
from re import fullmatch

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import User

# "auth" corresponds to the Blueprint's name
# "__name__" helps locate the root path of the Blueprint
bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Logs in the user if the correct email and password is inputted.

    :return: The rendered HTML of the Login Template.
    """

    if request.method == "POST":
        # Obtains the inputted email and password from the Login Form
        inputted_email = request.form["email"]
        inputted_password = request.form["password"]

        # Queries the database for the user by the inputted email
        user = User.query.filter_by(email=inputted_email).first()

        # Displays an error message if the inputted email is wrong/nonexistent
        if user:
            # Log ins the user if the correct password is inputted
            if check_password_hash(user.password, inputted_password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("site.home"))
            else:
                flash(
                    "Incorrect password. Please try again.", category="error"
                )
        else:
            flash("Email does not exist.", category="error")

    return render_template("auth/login.html", user=current_user)


@bp.route("/logout")
@login_required
def logout():
    """Logs out the user to the Login Page if he/she was already logged-in.

    :return: The rendered HTML of the Login Template.
    """

    logout_user()
    return redirect(url_for("auth.login"))


@bp.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    """Signs up the user if the valid email, name, and password are inputted.

    :return: The rendered HTML of the Home Template if all inputs are valid;
    otherwise, the rendered HTML of the Sign-Up Template is returned.
    """

    if request.method == "POST":
        # Obtains the inputted email, name, password, and confirm password
        # from the Sign-Up Form
        inputted_email = request.form["email"]
        inputted_name = request.form["name"]
        inputted_password = request.form["password"]
        inputted_confirm_password = request.form["confirm-password"]

        # Queries the database for the user by the inputted email
        user = User.query.filter_by(email=inputted_email).first()

        # Displays an error message if the specified condition isn't met;
        # otherwise, the user is signed-up and redirected to the Home Page.
        if user:
            flash("This email already exists.", category="error")
        elif not (
            inputted_email
            and inputted_name
            and inputted_password
            and inputted_confirm_password
        ):
            flash("No field can be empty.", category="error")
        elif len(inputted_email) < 4:
            flash(
                "Email must be greater than 3 characters long.",
                category="error",
            )
        elif len(inputted_name) > 255:
            flash(
                "Name must be less than 256 characters long.", category="error"
            )
        elif not fullmatch("[A-Za-z0-9!@#$%^&+=]{8,}", inputted_password):
            flash(
                "Password must be at least 8 characters long and restricted "
                "to uppercase letters, lowercase letters, numbers, and "
                "certain special characters (!@#$%^&+=).",
                category="error",
            )
        elif inputted_password != inputted_confirm_password:
            flash("The password fields don't match.", category="error")
        else:
            flash("Your account has been created!", category="success")
            new_user = User(
                email=inputted_email,
                name=inputted_name,
                password=generate_password_hash(
                    inputted_password, method="sha256"
                ),
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for("site.home"))

    return render_template("auth/sign_up.html", user=current_user)
