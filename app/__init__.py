import os
from pathlib import Path

from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from joblib import load

from app.models import db, User

bcrypt = Bcrypt()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "clave_temporal_desarrollo")

   db_url = os.environ.get("DATABASE_URL", "sqlite:///tickets.db")

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg://", 1)

if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Para continuar, primero tenés que iniciar sesión."
    login_manager.login_message_category = "warning"

    model_path = Path(__file__).resolve().parent.parent / "ml" / "priority_model.joblib"

    if model_path.exists():
        app.config["AI_PRIORITY_MODEL"] = load(model_path)
    else:
        app.config["AI_PRIORITY_MODEL"] = None

    from app.auth import auth_bp
    from app.tickets import tickets_bp
    from app.ai import ai_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tickets_bp)
    app.register_blueprint(ai_bp)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return redirect(url_for("tickets.dashboard"))

    return app