from datetime import date
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func, extract
from ..models import db, Transaction, Category

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@dashboard_bp.route("/dashboard")
@login_required  # F4
def index():
    today = date.today()

    # Totaalsaldo (F22)
    income_total = db.session.query(
        func.coalesce(func.sum(Transaction.amount), 0)
    ).join(Category).filter(
        Transaction.user_id == current_user.id,
        Category.type == "inkomst"
    ).scalar()

    expense_total = db.session.query(
        func.coalesce(func.sum(Transaction.amount), 0)
    ).join(Category).filter(
        Transaction.user_id == current_user.id,
        Category.type == "uitgave"
    ).scalar()

    balance = income_total - expense_total

    # Saldo huidige maand (F23)
    month_income = db.session.query(
        func.coalesce(func.sum(Transaction.amount), 0)
    ).join(Category).filter(
        Transaction.user_id == current_user.id,
        Category.type == "inkomst",
        extract("year", Transaction.date) == today.year,
        extract("month", Transaction.date) == today.month,
    ).scalar()

    month_expense = db.session.query(
        func.coalesce(func.sum(Transaction.amount), 0)
    ).join(Category).filter(
        Transaction.user_id == current_user.id,
        Category.type == "uitgave",
        extract("year", Transaction.date) == today.year,
        extract("month", Transaction.date) == today.month,
    ).scalar()

    # Laatste 10 transacties (F24)
    recent = Transaction.query.filter_by(user_id=current_user.id)\
        .order_by(Transaction.date.desc(), Transaction.id.desc())\
        .limit(10).all()

    return render_template(
        "dashboard.html",
        balance=balance,
        month_income=month_income,
        month_expense=month_expense,
        recent_transactions=recent,
        today=today,
    )


@dashboard_bp.route("/dashboard/chart-data")
@login_required
def chart_data():
    """JSON endpoint voor Chart.js grafieken (F25, F26)."""
    today = date.today()

    # Taartdiagram: uitgaven per categorie deze maand (F25)
    pie_rows = db.session.query(
        Category.name,
        func.coalesce(func.sum(Transaction.amount), 0).label("total")
    ).join(Transaction, Transaction.category_id == Category.id)\
     .filter(
        Transaction.user_id == current_user.id,
        Category.type == "uitgave",
        extract("year", Transaction.date) == today.year,
        extract("month", Transaction.date) == today.month,
     ).group_by(Category.name).all()

    pie_data = {"labels": [r.name for r in pie_rows], "values": [float(r.total) for r in pie_rows]}

    # Staafdiagram: inkomsten vs uitgaven per maand, laatste 6 maanden (F26)
    months, bar_income, bar_expense = [], [], []
    for i in range(5, -1, -1):
        m = today.month - i
        y = today.year
        while m <= 0:
            m += 12
            y -= 1

        inc = db.session.query(func.coalesce(func.sum(Transaction.amount), 0))\
            .join(Category).filter(
                Transaction.user_id == current_user.id,
                Category.type == "inkomst",
                extract("year", Transaction.date) == y,
                extract("month", Transaction.date) == m,
            ).scalar()

        exp = db.session.query(func.coalesce(func.sum(Transaction.amount), 0))\
            .join(Category).filter(
                Transaction.user_id == current_user.id,
                Category.type == "uitgave",
                extract("year", Transaction.date) == y,
                extract("month", Transaction.date) == m,
            ).scalar()

        months.append(f"{m:02d}/{y}")
        bar_income.append(float(inc))
        bar_expense.append(float(exp))

    bar_data = {"months": months, "income": bar_income, "expense": bar_expense}

    return jsonify({"pie": pie_data, "bar": bar_data})
