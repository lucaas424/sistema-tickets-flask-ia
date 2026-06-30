from pathlib import Path

import pandas as pd
from joblib import dump
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# Dataset simulado para el prototipo.
# La idea es entrenar un modelo simple que sugiera prioridad según impacto,
# urgencia, usuarios afectados y afectación del servicio.
data = [
    {"impacto": "Bajo", "urgencia": "Baja", "usuarios_afectados": 1, "afecta_servicio": "No", "prioridad_sugerida": "Baja"},
    {"impacto": "Bajo", "urgencia": "Baja", "usuarios_afectados": 2, "afecta_servicio": "No", "prioridad_sugerida": "Baja"},
    {"impacto": "Bajo", "urgencia": "Media", "usuarios_afectados": 3, "afecta_servicio": "No", "prioridad_sugerida": "Baja"},
    {"impacto": "Medio", "urgencia": "Baja", "usuarios_afectados": 4, "afecta_servicio": "No", "prioridad_sugerida": "Baja"},
    {"impacto": "Bajo", "urgencia": "Baja", "usuarios_afectados": 6, "afecta_servicio": "No", "prioridad_sugerida": "Baja"},
    {"impacto": "Bajo", "urgencia": "Media", "usuarios_afectados": 5, "afecta_servicio": "No", "prioridad_sugerida": "Baja"},

    {"impacto": "Medio", "urgencia": "Media", "usuarios_afectados": 5, "afecta_servicio": "No", "prioridad_sugerida": "Media"},
    {"impacto": "Medio", "urgencia": "Media", "usuarios_afectados": 10, "afecta_servicio": "No", "prioridad_sugerida": "Media"},
    {"impacto": "Medio", "urgencia": "Alta", "usuarios_afectados": 6, "afecta_servicio": "No", "prioridad_sugerida": "Media"},
    {"impacto": "Alto", "urgencia": "Baja", "usuarios_afectados": 8, "afecta_servicio": "No", "prioridad_sugerida": "Media"},
    {"impacto": "Medio", "urgencia": "Baja", "usuarios_afectados": 12, "afecta_servicio": "Sí", "prioridad_sugerida": "Media"},
    {"impacto": "Bajo", "urgencia": "Alta", "usuarios_afectados": 15, "afecta_servicio": "No", "prioridad_sugerida": "Media"},
    {"impacto": "Medio", "urgencia": "Media", "usuarios_afectados": 18, "afecta_servicio": "Sí", "prioridad_sugerida": "Media"},
    {"impacto": "Alto", "urgencia": "Media", "usuarios_afectados": 7, "afecta_servicio": "No", "prioridad_sugerida": "Media"},

    {"impacto": "Alto", "urgencia": "Alta", "usuarios_afectados": 20, "afecta_servicio": "Sí", "prioridad_sugerida": "Alta"},
    {"impacto": "Alto", "urgencia": "Alta", "usuarios_afectados": 30, "afecta_servicio": "Sí", "prioridad_sugerida": "Alta"},
    {"impacto": "Alto", "urgencia": "Media", "usuarios_afectados": 25, "afecta_servicio": "Sí", "prioridad_sugerida": "Alta"},
    {"impacto": "Medio", "urgencia": "Alta", "usuarios_afectados": 35, "afecta_servicio": "Sí", "prioridad_sugerida": "Alta"},
    {"impacto": "Alto", "urgencia": "Alta", "usuarios_afectados": 12, "afecta_servicio": "Sí", "prioridad_sugerida": "Alta"},
    {"impacto": "Alto", "urgencia": "Alta", "usuarios_afectados": 18, "afecta_servicio": "No", "prioridad_sugerida": "Alta"},
    {"impacto": "Medio", "urgencia": "Alta", "usuarios_afectados": 22, "afecta_servicio": "Sí", "prioridad_sugerida": "Alta"},
    {"impacto": "Alto", "urgencia": "Media", "usuarios_afectados": 40, "afecta_servicio": "Sí", "prioridad_sugerida": "Alta"},

    {"impacto": "Bajo", "urgencia": "Baja", "usuarios_afectados": 0, "afecta_servicio": "No", "prioridad_sugerida": "Baja"},
    {"impacto": "Bajo", "urgencia": "Media", "usuarios_afectados": 8, "afecta_servicio": "No", "prioridad_sugerida": "Media"},
    {"impacto": "Medio", "urgencia": "Alta", "usuarios_afectados": 9, "afecta_servicio": "No", "prioridad_sugerida": "Media"},
    {"impacto": "Alto", "urgencia": "Baja", "usuarios_afectados": 16, "afecta_servicio": "Sí", "prioridad_sugerida": "Media"},
    {"impacto": "Alto", "urgencia": "Alta", "usuarios_afectados": 45, "afecta_servicio": "Sí", "prioridad_sugerida": "Alta"},
    {"impacto": "Medio", "urgencia": "Media", "usuarios_afectados": 2, "afecta_servicio": "No", "prioridad_sugerida": "Baja"},
    {"impacto": "Medio", "urgencia": "Alta", "usuarios_afectados": 28, "afecta_servicio": "Sí", "prioridad_sugerida": "Alta"},
    {"impacto": "Bajo", "urgencia": "Alta", "usuarios_afectados": 4, "afecta_servicio": "No", "prioridad_sugerida": "Media"},
]


df = pd.DataFrame(data)

X = df[["impacto", "urgencia", "usuarios_afectados", "afecta_servicio"]]
y = df["prioridad_sugerida"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y,
)

categorical_features = ["impacto", "urgencia", "afecta_servicio"]
numeric_features = ["usuarios_afectados"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", StandardScaler(), numeric_features),
    ]
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
    ]
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred, zero_division=0))

model_path = Path(__file__).resolve().parent / "priority_model.joblib"
dump(model, model_path)

print(f"\nModelo entrenado y guardado correctamente en: {model_path}")