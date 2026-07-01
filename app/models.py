from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(30), nullable=False, default="Administrador")
    activo = db.Column(db.Boolean, nullable=False, default=True)
    fecha_alta = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    tickets = db.relationship("Ticket", backref="creador", lazy=True)

    def __init__(self, nombre, email, password_hash, rol="Administrador"):
        self.nombre = nombre
        self.email = email
        self.password_hash = password_hash
        self.rol = rol


class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    prioridad = db.Column(db.String(20), nullable=False)

    estado = db.Column(db.String(30), nullable=False, default="Abierto")

    impacto = db.Column(db.String(20), nullable=False)
    urgencia = db.Column(db.String(20), nullable=False)

    usuarios_afectados = db.Column(db.Integer, nullable=False, default=0)
    afecta_servicio = db.Column(db.Boolean, nullable=False, default=False)

    comentario_cierre = db.Column(db.Text, nullable=True)

    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_cierre = db.Column(db.DateTime, nullable=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    def __init__(
        self,
        titulo,
        descripcion,
        categoria,
        prioridad,
        impacto,
        urgencia,
        usuarios_afectados,
        afecta_servicio,
        usuario_id,
    ):
        self.titulo = titulo
        self.descripcion = descripcion
        self.categoria = categoria
        self.prioridad = prioridad
        self.impacto = impacto
        self.urgencia = urgencia
        self.usuarios_afectados = usuarios_afectados
        self.afecta_servicio = afecta_servicio
        self.usuario_id = usuario_id

    def actualizar_fecha(self):
        self.fecha_actualizacion = datetime.utcnow()

    def esta_cerrado(self):
        return self.estado == "Cerrado"