# TicketFlow IA

Prototipo funcional desarrollado en Flask para la gestión de tickets de soporte técnico, con login seguro, CRUD completo e integración de Inteligencia Artificial mediante un modelo de Machine Learning entrenado con Scikit-Learn.

## Objetivo del proyecto

El objetivo del sistema es permitir la registración, consulta, modificación, cierre y eliminación de tickets de soporte técnico. Además, incorpora una funcionalidad de IA que sugiere una prioridad inicial para un ticket en base a variables como impacto, urgencia, cantidad de usuarios afectados y afectación del servicio.

Este prototipo corresponde a una versión mínima funcional, enfocada en demostrar la trazabilidad del requisito principal desde la base de datos hasta la interfaz web.

## Funcionalidades principales

- Registro de usuarios.
- Inicio y cierre de sesión.
- Contraseñas protegidas con Bcrypt.
- Panel principal con resumen de tickets.
- CRUD completo de tickets:
  - Crear ticket.
  - Listar tickets.
  - Ver detalle.
  - Editar ticket.
  - Cerrar ticket.
  - Eliminar ticket.
- Filtros por título, estado y prioridad.
- Mensajes visuales para acciones exitosas o errores.
- Modelo de IA integrado para sugerir prioridad.
- Estructura modular con Blueprints.
- Uso de App Factory.
- Configuración mediante variables de entorno.
- Preparado para despliegue en Render con PostgreSQL.

## Tecnologías utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Bcrypt
- Jinja2
- SQLite para desarrollo local
- PostgreSQL para producción
- Scikit-Learn
- Pandas
- Joblib
- Gunicorn
- Render

## Integración de IA

El sistema utiliza un modelo de regresión logística entrenado previamente con Scikit-Learn.  
El modelo fue serializado con Joblib y luego cargado automáticamente al iniciar la aplicación Flask.

La predicción de prioridad toma como entrada:

- Impacto
- Urgencia
- Cantidad de usuarios afectados
- Si el servicio está afectado o no

Como salida, el sistema devuelve una prioridad sugerida:

- Baja
- Media
- Alta

También muestra un nivel de confianza estimado para acompañar la decisión.

## Estructura del proyecto

```text
sistema-tickets-flask-ia/
│
├── app/
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── tickets.html
│   │   ├── ticket_form.html
│   │   ├── ticket_detail.html
│   │   └── ai_priority.html
│   │
│   ├── __init__.py
│   ├── models.py
│   ├── auth.py
│   ├── tickets.py
│   └── ai.py
│
├── ml/
│   ├── train_model.py
│   └── priority_model.joblib
│
├── run.py
├── requirements.txt
├── render.yaml
├── .gitignore
├── .env.example
└── README.md
