import os
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from .models import db, User, Category, DEFAULT_CATEGORIES
from config import config

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Log eerst in om deze pagina te bekijken."
login_manager.login_message_category = "warning"

migrate = Migrate()
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app(env=None):
    app = Flask(__name__, instance_relative_config=True, template_folder="../templates", static_folder="../static")

    env = env or os.environ.get("FLASK_ENV", "default")
    app.config.from_object(config[env])

    # Zorg dat instance/ map bestaat
    os.makedirs(app.instance_path, exist_ok=True)

    # Extensions initialiseren
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Blueprints registreren
    from .auth.routes import auth_bp
    from .dashboard.routes import dashboard_bp
    from .transactions.routes import transactions_bp
    from .categories.routes import categories_bp
    from .profile.routes import profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(profile_bp)

    # Tabellen aanmaken bij eerste start
    with app.app_context():
        db.create_all()

    return app
