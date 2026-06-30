from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app import bcrypt
from app.models import db, User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("Ya tenés una sesión iniciada.", "info")
        return redirect(url_for("tickets.dashboard"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        if not nombre or not email or not password:
            flash("Completá todos los campos para crear la cuenta.", "warning")
            return render_template("register.html")

        if len(password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "warning")
            return render_template("register.html")

        usuario_existente = User.query.filter_by(email=email).first()

        if usuario_existente:
            flash("Ya existe una cuenta registrada con ese email.", "danger")
            return render_template("register.html")

        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        nuevo_usuario = User(
            nombre=nombre,
            email=email,
            password_hash=password_hash,
            rol="Administrador"
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Cuenta creada exitosamente. Ya podés iniciar sesión.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("Ya estás dentro del sistema.", "info")
        return redirect(url_for("tickets.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        if not email or not password:
            flash("Ingresá email y contraseña para continuar.", "warning")
            return render_template("login.html")

        usuario = User.query.filter_by(email=email).first()

        if not usuario:
            flash("Email o contraseña incorrectos.", "danger")
            return render_template("login.html")

        if not usuario.activo:
            flash("El usuario se encuentra inactivo. Contactá al administrador.", "danger")
            return render_template("login.html")

        password_correcta = bcrypt.check_password_hash(usuario.password_hash, password)

        if not password_correcta:
            flash("Email o contraseña incorrectos.", "danger")
            return render_template("login.html")

        login_user(usuario)
        flash(f"Bienvenido, {usuario.nombre}. Iniciaste sesión correctamente.", "success")
        return redirect(url_for("tickets.dashboard"))

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    nombre = current_user.nombre
    logout_user()
    flash(f"Sesión cerrada correctamente. Hasta luego, {nombre}.", "info")
    return redirect(url_for("auth.login"))