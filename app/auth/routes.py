import re
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from ..models import db, User, Category, DEFAULT_CATEGORIES

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

PASSWORD_RE = re.compile(r"^(?=.*[A-Z])(?=.*\d).{8,}$")  # NF7


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Validatie (F40, F41, NF7)
        if not username or not email or not password:
            flash("Vul alle verplichte velden in.", "danger")
            return render_template("auth/register.html")

        if User.query.filter_by(username=username).first():
            flash("Gebruikersnaam is al in gebruik.", "danger")
            return render_template("auth/register.html")

        if User.query.filter_by(email=email).first():
            flash("E-mailadres is al in gebruik.", "danger")
            return render_template("auth/register.html")

        if not PASSWORD_RE.match(password):
            flash("Wachtwoord moet minimaal 8 tekens, 1 hoofdletter en 1 cijfer bevatten.", "danger")
            return render_template("auth/register.html")

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()  # Verkrijg user.id vóór commit

        # Standaardcategorieën aanmaken (F9)
        for cat in DEFAULT_CATEGORIES:
            db.session.add(Category(name=cat["name"], type=cat["type"], user_id=user.id))

        db.session.commit()
        flash("Registratie geslaagd! Je kunt nu inloggen.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()
        password = request.form.get("password", "")

        if not identifier or not password:
            flash("Vul alle velden in.", "danger")
            return render_template("auth/login.html")

        # Inloggen met gebruikersnaam of e-mail (F3)
        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier.lower())
        ).first()

        if user is None or not user.check_password(password):
            flash("Onjuiste gebruikersnaam/e-mail of wachtwoord.", "danger")
            return render_template("auth/login.html")

        login_user(user)
        next_page = request.args.get("next")
        flash(f"Welkom terug, {user.username}!", "success")
        return redirect(next_page or url_for("dashboard.index"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Je bent uitgelogd.", "info")
    return redirect(url_for("auth.login"))
