import csv
import io
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, Response
from flask_login import login_required, current_user
from ..models import db, Transaction, Category

transactions_bp = Blueprint("transactions", __name__, url_prefix="/transactions")


def _get_user_categories():
    return Category.query.filter_by(user_id=current_user.id).order_by(Category.name).all()


def _parse_amount(raw):
    """Valideer en geef Decimal bedrag terug, of None bij fout."""
    try:
        val = Decimal(raw.replace(",", "."))
        if val <= 0:
            return None
        # Max 2 decimalen (F43)
        if val != val.quantize(Decimal("0.01")):
            return None
        return val
    except (InvalidOperation, AttributeError):
        return None


@transactions_bp.route("/")
@login_required  # F4
def list_transactions():
    query = Transaction.query.filter_by(user_id=current_user.id)

    # Filteren (F29, F30, F31, F32)
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    category_id = request.args.get("category_id")
    tx_type = request.args.get("type")
    keyword = request.args.get("q", "").strip()

    if date_from:
        try:
            query = query.filter(Transaction.date >= datetime.strptime(date_from, "%Y-%m-%d").date())
        except ValueError:
            pass

    if date_to:
        try:
            query = query.filter(Transaction.date <= datetime.strptime(date_to, "%Y-%m-%d").date())
        except ValueError:
            pass

    if category_id:
        query = query.filter(Transaction.category_id == category_id)

    if tx_type in ("inkomst", "uitgave"):
        query = query.join(Category).filter(Category.type == tx_type)

    if keyword:
        query = query.filter(Transaction.description.ilike(f"%{keyword}%"))

    # Sorteren (F35)
    sort = request.args.get("sort", "date_desc")
    if sort == "date_asc":
        query = query.order_by(Transaction.date.asc())
    elif sort == "amount_desc":
        query = query.order_by(Transaction.amount.desc())
    elif sort == "amount_asc":
        query = query.order_by(Transaction.amount.asc())
    else:
        query = query.order_by(Transaction.date.desc(), Transaction.id.desc())

    transactions = query.all()
    categories = _get_user_categories()

    return render_template(
        "transactions/list.html",
        transactions=transactions,
        categories=categories,
        filters=request.args,
    )


@transactions_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    categories = _get_user_categories()

    if request.method == "POST":
        amount_raw = request.form.get("amount", "").strip()
        date_raw = request.form.get("date", "").strip()
        description = request.form.get("description", "").strip()[:200]  # F21
        category_id = request.form.get("category_id")

        # Validatie (F41)
        if not amount_raw or not date_raw or not category_id:
            flash("Vul alle verplichte velden in.", "danger")
            return render_template("transactions/form.html", categories=categories, action="add")

        amount = _parse_amount(amount_raw)
        if amount is None:
            flash("Bedrag moet een positief getal zijn met maximaal 2 decimalen.", "danger")  # F20, F43
            return render_template("transactions/form.html", categories=categories, action="add")

        try:
            tx_date = datetime.strptime(date_raw, "%Y-%m-%d").date()
        except ValueError:
            flash("Ongeldige datum.", "danger")
            return render_template("transactions/form.html", categories=categories, action="add")

        # Controleer of categorie van deze gebruiker is
        cat = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
        if not cat:
            abort(403)

        tx = Transaction(
            amount=amount,
            date=tx_date,
            description=description or None,
            user_id=current_user.id,
            category_id=cat.id,
        )
        db.session.add(tx)
        db.session.commit()
        flash("Transactie toegevoegd.", "success")  # F48
        return redirect(url_for("transactions.list_transactions"))

    return render_template("transactions/form.html", categories=categories, action="add")


@transactions_bp.route("/<int:tx_id>/edit", methods=["GET", "POST"])
@login_required
def edit(tx_id):
    tx = Transaction.query.filter_by(id=tx_id, user_id=current_user.id).first_or_404()
    categories = _get_user_categories()

    if request.method == "POST":
        amount_raw = request.form.get("amount", "").strip()
        date_raw = request.form.get("date", "").strip()
        description = request.form.get("description", "").strip()[:200]
        category_id = request.form.get("category_id")

        if not amount_raw or not date_raw or not category_id:
            flash("Vul alle verplichte velden in.", "danger")
            return render_template("transactions/form.html", tx=tx, categories=categories, action="edit")

        amount = _parse_amount(amount_raw)
        if amount is None:
            flash("Bedrag moet een positief getal zijn met maximaal 2 decimalen.", "danger")
            return render_template("transactions/form.html", tx=tx, categories=categories, action="edit")

        try:
            tx_date = datetime.strptime(date_raw, "%Y-%m-%d").date()
        except ValueError:
            flash("Ongeldige datum.", "danger")
            return render_template("transactions/form.html", tx=tx, categories=categories, action="edit")

        cat = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
        if not cat:
            abort(403)

        tx.amount = amount
        tx.date = tx_date
        tx.description = description or None
        tx.category_id = cat.id
        db.session.commit()
        flash("Transactie bijgewerkt.", "success")
        return redirect(url_for("transactions.list_transactions"))

    return render_template("transactions/form.html", tx=tx, categories=categories, action="edit")


@transactions_bp.route("/<int:tx_id>/delete", methods=["POST"])
@login_required
def delete(tx_id):
    tx = Transaction.query.filter_by(id=tx_id, user_id=current_user.id).first_or_404()
    db.session.delete(tx)
    db.session.commit()
    flash("Transactie verwijderd.", "success")
    return redirect(url_for("transactions.list_transactions"))


@transactions_bp.route("/export/csv")
@login_required  # F36, F38
def export_csv():
    transactions = Transaction.query.filter_by(user_id=current_user.id)\
        .order_by(Transaction.date.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Datum", "Beschrijving", "Categorie", "Type", "Bedrag"])

    for tx in transactions:
        writer.writerow([
            tx.date.strftime("%d-%m-%Y"),
            tx.description or "",
            tx.category.name,
            tx.category.type,
            str(tx.amount),
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=transacties.csv"},
    )
