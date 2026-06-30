from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.models import db, Ticket

def convertir_si_no_a_booleano(valor):
    return str(valor).strip().lower() in ["sí", "si", "true", "1", "on", "yes"]

tickets_bp = Blueprint("tickets", __name__)


@tickets_bp.route("/dashboard")
@login_required
def dashboard():
    total_tickets = Ticket.query.count()
    abiertos = Ticket.query.filter_by(estado="Abierto").count()
    en_proceso = Ticket.query.filter_by(estado="En proceso").count()
    cerrados = Ticket.query.filter_by(estado="Cerrado").count()

    ultimos_tickets = Ticket.query.order_by(Ticket.fecha_creacion.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        total_tickets=total_tickets,
        abiertos=abiertos,
        en_proceso=en_proceso,
        cerrados=cerrados,
        ultimos_tickets=ultimos_tickets,
    )


@tickets_bp.route("/tickets")
@login_required
def listar_tickets():
    estado = request.args.get("estado", "")
    prioridad = request.args.get("prioridad", "")
    busqueda = request.args.get("busqueda", "")

    consulta = Ticket.query

    if estado:
        consulta = consulta.filter(Ticket.estado == estado)

    if prioridad:
        consulta = consulta.filter(Ticket.prioridad == prioridad)

    if busqueda:
        consulta = consulta.filter(Ticket.titulo.ilike(f"%{busqueda}%"))

    tickets = consulta.order_by(Ticket.fecha_creacion.desc()).all()

    return render_template(
        "tickets.html",
        tickets=tickets,
        estado=estado,
        prioridad=prioridad,
        busqueda=busqueda,
    )


@tickets_bp.route("/tickets/nuevo", methods=["GET", "POST"])
@login_required
def crear_ticket():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        categoria = request.form.get("categoria", "").strip()
        prioridad = request.form.get("prioridad", "").strip()
        impacto = request.form.get("impacto", "").strip()
        urgencia = request.form.get("urgencia", "").strip()
        usuarios_afectados = request.form.get("usuarios_afectados", "0")
        afecta_servicio = convertir_si_no_a_booleano(request.form.get("afecta_servicio"))

        if not titulo or not descripcion or not categoria or not prioridad or not impacto or not urgencia:
            flash("Complete todos los campos obligatorios antes de guardar el ticket.", "warning")
            return render_template("ticket_form.html", ticket=None, modo="crear")

        try:
            usuarios_afectados = int(usuarios_afectados)
        except ValueError:
            usuarios_afectados = 0

        nuevo_ticket = Ticket(
            titulo=titulo,
            descripcion=descripcion,
            categoria=categoria,
            prioridad=prioridad,
            impacto=impacto,
            urgencia=urgencia,
            usuarios_afectados=usuarios_afectados,
            afecta_servicio=afecta_servicio,
            usuario_id=current_user.id,
        )

        db.session.add(nuevo_ticket)
        db.session.commit()

        flash("Ticket creado correctamente. Ya se encuentra disponible para seguimiento.", "success")
        return redirect(url_for("tickets.listar_tickets"))

    return render_template("ticket_form.html", ticket=None, modo="crear")


@tickets_bp.route("/tickets/<int:id>")
@login_required
def detalle_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    return render_template("ticket_detail.html", ticket=ticket)


@tickets_bp.route("/tickets/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar_ticket(id):
    ticket = Ticket.query.get_or_404(id)

    if request.method == "POST":
        ticket.titulo = request.form.get("titulo", "").strip()
        ticket.descripcion = request.form.get("descripcion", "").strip()
        ticket.categoria = request.form.get("categoria", "").strip()
        ticket.prioridad = request.form.get("prioridad", "").strip()
        ticket.impacto = request.form.get("impacto", "").strip()
        ticket.urgencia = request.form.get("urgencia", "").strip()
        ticket.estado = request.form.get("estado", "Abierto")
        ticket.afecta_servicio = convertir_si_no_a_booleano(request.form.get("afecta_servicio"))

        try:
            ticket.usuarios_afectados = int(request.form.get("usuarios_afectados", 0))
        except ValueError:
            ticket.usuarios_afectados = 0

        ticket.actualizar_fecha()

        if ticket.estado == "Cerrado" and ticket.fecha_cierre is None:
            ticket.fecha_cierre = datetime.utcnow()

        if ticket.estado != "Cerrado":
            ticket.fecha_cierre = None

        db.session.commit()

        flash("Ticket actualizado correctamente.", "success")
        return redirect(url_for("tickets.detalle_ticket", id=ticket.id))

    return render_template("ticket_form.html", ticket=ticket, modo="editar")


@tickets_bp.route("/tickets/<int:id>/cerrar", methods=["POST"])
@login_required
def cerrar_ticket(id):
    ticket = Ticket.query.get_or_404(id)

    if ticket.estado == "Cerrado":
        flash("El ticket ya se encontraba cerrado.", "info")
        return redirect(url_for("tickets.detalle_ticket", id=ticket.id))

    ticket.estado = "Cerrado"
    ticket.fecha_cierre = datetime.utcnow()
    ticket.actualizar_fecha()

    db.session.commit()

    flash("Ticket cerrado correctamente.", "success")
    return redirect(url_for("tickets.detalle_ticket", id=ticket.id))


@tickets_bp.route("/tickets/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar_ticket(id):
    ticket = Ticket.query.get_or_404(id)

    db.session.delete(ticket)
    db.session.commit()

    flash("Ticket eliminado correctamente.", "success")
    return redirect(url_for("tickets.listar_tickets"))