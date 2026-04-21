from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, logout_user
from ..models import db, User

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


@profile_bp.route("/")
@login_required
def view():
    return render_template("profile.html")


@profile_bp.route("/change-password", methods=["POST"])
@login_required
def change_password():
    old_pw = request.form.get("old_password", "")
    new_pw = request.form.get("new_password", "")
    confirm_pw = request.form.get("confirm_password", "")

    if not current_user.check_password(old_pw):
        flash("Huidig wachtwoord is onjuist.", "danger")
        return redirect(url_for("profile.view"))

    if new_pw != confirm_pw:
        flash("Nieuwe wachtwoorden komen niet overeen.", "danger")
        return redirect(url_for("profile.view"))

    if len(new_pw) < 8:
        flash("Nieuw wachtwoord moet minimaal 8 tekens bevatten.", "danger")
        return redirect(url_for("profile.view"))

    current_user.set_password(new_pw)
    db.session.commit()
    flash("Wachtwoord gewijzigd.", "success")
    return redirect(url_for("profile.view"))


@profile_bp.route("/delete", methods=["POST"])
@login_required
def delete_account():
    user = User.query.get(current_user.id)
    logout_user()
    db.session.delete(user)  # cascade verwijdert ook transacties & categorieën (F8)
    db.session.commit()
    flash("Account verwijderd.", "info")
    return redirect(url_for("auth.login"))
