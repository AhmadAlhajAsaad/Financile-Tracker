from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Standaard categorieën die elke nieuwe gebruiker krijgt (F9)
DEFAULT_CATEGORIES = [
    {"name": "Salaris",        "type": "inkomst"},
    {"name": "Boodschappen",   "type": "uitgave"},
    {"name": "Huur",           "type": "uitgave"},
    {"name": "Vervoer",        "type": "uitgave"},
    {"name": "Eten buiten",    "type": "uitgave"},
]


class User(UserMixin, db.Model):
    """Gebruikersmodel (F1, F2, F6, F7, F8)."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    categories = db.relationship(
        "Category", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    transactions = db.relationship(
        "Transaction", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def set_password(self, password):
        """Hash en sla wachtwoord op (F2, NF8)."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Category(db.Model):
    """Categorie per gebruiker (F9–F13)."""
    __tablename__ = "categories"
    __table_args__ = (
        db.Index("ix_categories_user_id", "user_id"),  # NF1
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)   # "inkomst" of "uitgave"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    transactions = db.relationship("Transaction", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category {self.name} ({self.type})>"


class Transaction(db.Model):
    """Transactiemodel (F14–F21)."""
    __tablename__ = "transactions"
    __table_args__ = (
        db.Index("ix_transactions_user_id", "user_id"),        # NF1
        db.Index("ix_transactions_date", "date"),              # NF1
        db.Index("ix_transactions_category_id", "category_id"), # NF1
    )

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)       # F20, F43
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(200), nullable=True)      # F21
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Transaction {self.amount} on {self.date}>"
