import pandas as pd
from flask import Blueprint, current_app, flash, jsonify, render_template, request
from flask_login import login_required


ai_bp = Blueprint("ai", __name__)


def predecir_prioridad(impacto, urgencia, usuarios_afectados, afecta_servicio):
    model = current_app.config.get("AI_PRIORITY_MODEL")

    if model is None:
        return None, None, {}

    entrada = pd.DataFrame(
        [
            {
                "impacto": impacto,
                "urgencia": urgencia,
                "usuarios_afectados": usuarios_afectados,
                "afecta_servicio": afecta_servicio,
            }
        ]
    )

    prioridad = model.predict(entrada)[0]

    probabilidades = {}

    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(entrada)[0]
        clases = model.classes_

        probabilidades = {
            clase: round(float(valor) * 100, 2)
            for clase, valor in zip(clases, proba)
        }

        confianza = max(probabilidades.values())
    else:
        confianza = None

    return prioridad, confianza, probabilidades


@ai_bp.route("/ia/prioridad", methods=["GET", "POST"])
@login_required
def prediccion_prioridad():
    resultado = None
    confianza = None
    probabilidades = {}

    datos = {
        "impacto": "",
        "urgencia": "",
        "usuarios_afectados": "",
        "afecta_servicio": "No",
    }

    if request.method == "POST":
        datos["impacto"] = request.form.get("impacto", "").strip()
        datos["urgencia"] = request.form.get("urgencia", "").strip()
        datos["usuarios_afectados"] = request.form.get("usuarios_afectados", "").strip()
        datos["afecta_servicio"] = request.form.get("afecta_servicio", "No").strip()

        if not datos["impacto"] or not datos["urgencia"] or not datos["usuarios_afectados"]:
            flash("Complete impacto, urgencia y usuarios afectados para generar la predicción.", "warning")
            return render_template(
                "ai_priority.html",
                resultado=resultado,
                confianza=confianza,
                probabilidades=probabilidades,
                datos=datos,
            )

        try:
            usuarios_afectados = int(datos["usuarios_afectados"])
        except ValueError:
            flash("La cantidad de usuarios afectados debe ser un número válido.", "danger")
            return render_template(
                "ai_priority.html",
                resultado=resultado,
                confianza=confianza,
                probabilidades=probabilidades,
                datos=datos,
            )

        resultado, confianza, probabilidades = predecir_prioridad(
            datos["impacto"],
            datos["urgencia"],
            usuarios_afectados,
            datos["afecta_servicio"],
        )

        if resultado is None:
            flash("El modelo de IA todavía no está disponible. Primero se debe entrenar el modelo.", "danger")
        else:
            flash("Predicción generada correctamente.", "success")

    return render_template(
        "ai_priority.html",
        resultado=resultado,
        confianza=confianza,
        probabilidades=probabilidades,
        datos=datos,
    )


@ai_bp.route("/api/prioridad", methods=["POST"])
@login_required
def api_prediccion_prioridad():
    data = request.get_json(silent=True) or {}

    impacto = data.get("impacto")
    urgencia = data.get("urgencia")
    afecta_servicio = data.get("afecta_servicio", "No")

    try:
        usuarios_afectados = int(data.get("usuarios_afectados", 0))
    except ValueError:
        return jsonify({"error": "usuarios_afectados debe ser numérico"}), 400

    if not impacto or not urgencia:
        return jsonify({"error": "impacto y urgencia son obligatorios"}), 400

    resultado, confianza, probabilidades = predecir_prioridad(
        impacto,
        urgencia,
        usuarios_afectados,
        afecta_servicio,
    )

    if resultado is None:
        return jsonify({"error": "Modelo de IA no disponible"}), 500

    return jsonify(
        {
            "prioridad_sugerida": resultado,
            "confianza": confianza,
            "probabilidades": probabilidades,
        }
    )