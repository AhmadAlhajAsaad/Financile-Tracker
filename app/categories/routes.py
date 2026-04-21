from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import db, Category

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")


@categories_bp.route("/")
@login_required
def manage():
    categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.type, Category.name).all()
    return render_template("categories/manage.html", categories=categories)


@categories_bp.route("/add", methods=["POST"])
@login_required
def add():
    name = request.form.get("name", "").strip()
    cat_type = request.form.get("type", "").strip()

    if not name or cat_type not in ("inkomst", "uitgave"):
        flash("Vul een geldige naam en type in.", "danger")
        return redirect(url_for("categories.manage"))

    db.session.add(Category(name=name, type=cat_type, user_id=current_user.id))
    db.session.commit()
    flash(f'Categorie "{name}" aangemaakt.', "success")
    return redirect(url_for("categories.manage"))


@categories_bp.route("/<int:cat_id>/edit", methods=["POST"])
@login_required
def edit(cat_id):
    cat = Category.query.filter_by(id=cat_id, user_id=current_user.id).first_or_404()
    name = request.form.get("name", "").strip()

    if not name:
        flash("Naam mag niet leeg zijn.", "danger")
        return redirect(url_for("categories.manage"))

    cat.name = name
    db.session.commit()
    flash("Categorie bijgewerkt.", "success")
    return redirect(url_for("categories.manage"))


@categories_bp.route("/<int:cat_id>/delete", methods=["POST"])
@login_required
def delete(cat_id):
    cat = Category.query.filter_by(id=cat_id, user_id=current_user.id).first_or_404()

    # Blokkeer verwijderen als er transacties aan hangen (F12, F42)
    if cat.transactions:
        flash("Kan categorie niet verwijderen: er zijn nog transacties aan gekoppeld.", "danger")
        return redirect(url_for("categories.manage"))

    db.session.delete(cat)
    db.session.commit()
    flash("Categorie verwijderd.", "success")
    return redirect(url_for("categories.manage"))
