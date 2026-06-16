import csv
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List


CSV_PATH = Path("respuestas_estudiantes.csv")


def performance_level(percentage: float) -> str:
    if percentage < 60:
        return "Bajo"
    if percentage < 80:
        return "Basico"
    if percentage < 90:
        return "Alto"
    return "Superior"


def general_feedback(level: str) -> str:
    feedback = {
        "Bajo": "Conviene repasar los conceptos base: arbol de juego, utilidad, roles MAX/MIN y diferencia entre Minimax y Alfa-Beta.",
        "Basico": "Hay una comprension inicial solida. El siguiente paso es justificar por que Alfa-Beta conserva la decision optima explorando menos.",
        "Alto": "Buen dominio conceptual. Puedes profundizar en heuristicas, profundidad limitada e informacion imperfecta.",
        "Superior": "Excelente desempeno. El reto siguiente es transferir estas ideas a juegos mas grandes o contextos de decision reales.",
    }
    return feedback[level]


def slugify_name(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", name.strip()).strip("_").lower()
    return cleaned or "estudiante"


def now_label() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def build_evidence_markdown(data: Dict[str, str]) -> str:
    return f"""# Evidencia Unidad 3: Busqueda en juegos y agentes adversarios

Fecha y hora de generacion: {data['timestamp']}

## Datos del estudiante

- Nombre: {data['name']}
- Codigo: {data['student_id']}
- Grupo: {data['group']}
- Correo: {data['email']}

## Resumen del modulo

Master class: Jugadas Inteligentes: Estrategias Optimas en Juegos a traves de la Busqueda.

Resultado de aprendizaje: El estudiante analiza y aplica algoritmos de busqueda en juegos, considerando complejidad, eficiencia y optimizacion.

El laboratorio integro busqueda adversarial, Minimax, poda Alfa-Beta, informacion imperfecta, juegos en tiempo real y reflexion sobre agentes inteligentes.

## Resultado del quiz

- Puntaje: {data['quiz_score']} de {data['quiz_total']}
- Porcentaje: {data['quiz_percentage']}%
- Nivel de desempeno: {data['level']}
- Retroalimentacion automatica: {data['feedback']}

## Laboratorio interactivo

- Estrategia usada: {data['strategy']}
- Resultado de la partida: {data['game_result']}
- Nodos Minimax maximos observados: {data['minimax_nodes']}
- Nodos Alfa-Beta maximos observados: {data['alphabeta_nodes']}
- Ramas podadas maximas observadas: {data['pruned']}
- Comparacion: {data['comparison']}

## Historial de jugadas y explicaciones

{data['move_history']}

## Respuestas del quiz

{data['quiz_answers']}

## Reflexion sobre juegos en tiempo real

{data['real_time_reflection']}

## Reflexion final del estudiante

{data['final_reflection']}

## Lecciones aprendidas

{data['lessons']}
"""


def append_student_response(row: Dict[str, str]) -> None:
    fields: List[str] = [
        "fecha_hora",
        "nombre",
        "codigo",
        "grupo",
        "correo",
        "puntaje_quiz",
        "porcentaje",
        "nivel_desempeno",
        "reflexion_tiempo_real",
        "reflexion_final",
        "estrategia_usada",
        "nodos_minimax",
        "nodos_alphabeta",
        "ramas_podadas",
    ]
    file_exists = CSV_PATH.exists()
    with CSV_PATH.open("a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        if not file_exists:
            writer.writeheader()
        writer.writerow({field: row.get(field, "") for field in fields})
