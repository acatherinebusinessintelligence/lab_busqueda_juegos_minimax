from dataclasses import dataclass
from typing import Dict, List, Optional


TARGET = 10
MOVES = (1, 2, 3)
HUMAN_PLAYER = "Estudiante"
AI_PLAYER = "IA"


@dataclass
class RaceResult:
    score: int
    move: Optional[int]
    nodes: int


def legal_moves(total: int) -> List[int]:
    return [move for move in MOVES if total + move <= TARGET]


def is_terminal(total: int) -> bool:
    return total == TARGET


def minimax_race(total: int, is_ai_turn: bool, counter: Dict[str, int]) -> tuple[int, Optional[int]]:
    counter["nodes"] += 1
    if is_terminal(total):
        return (-1 if is_ai_turn else 1), None

    moves = legal_moves(total)
    if not moves:
        return 0, None

    if is_ai_turn:
        best_score = -2
        best_move = None
        for move in moves:
            score, _ = minimax_race(total + move, False, counter)
            if score > best_score:
                best_score = score
                best_move = move
        return best_score, best_move

    best_score = 2
    best_move = None
    for move in moves:
        score, _ = minimax_race(total + move, True, counter)
        if score < best_score:
            best_score = score
            best_move = move
    return best_score, best_move


def best_race_move(total: int) -> RaceResult:
    counter = {"nodes": 0}
    score, move = minimax_race(total, True, counter)
    return RaceResult(score=score, move=move, nodes=counter["nodes"])


def evaluate_race_options(total: int) -> List[Dict[str, str]]:
    rows = []
    for move in legal_moves(total):
        counter = {"nodes": 0}
        score, _ = minimax_race(total + move, False, counter)
        rows.append(
            {
                "Opcion IA": f"+{move}",
                "Nuevo estado": str(total + move),
                "Valor Minimax": str(score),
                "Resultado esperado": interpret_race_score(score),
                "Interpretacion pedagogica": explain_race_option(total, move, score),
                "Nodos explorados": str(counter["nodes"]),
            }
        )
    return rows


def interpret_race_score(score: int) -> str:
    if score == 1:
        return "Victoria posible para IA"
    if score == 0:
        return "Empate o estado neutro"
    return "Riesgo de derrota"


def explain_race_option(total: int, move: int, score: int) -> str:
    new_total = total + move
    if new_total == TARGET:
        return "Llega directamente a 10; es un estado terminal ganador para quien realiza la jugada."
    if score == 1:
        return f"Al pasar de {total} a {new_total}, la IA conserva una ruta ganadora si responde de forma optima."
    if score == 0:
        return f"Al pasar de {total} a {new_total}, la posicion queda equilibrada y depende de las siguientes respuestas."
    return f"Al pasar de {total} a {new_total}, el estudiante podria forzar una ruta favorable si juega bien."


def explain_human_race_move(total_before: int, move: int) -> Dict[str, str]:
    total_after = total_before + move
    if total_after == TARGET:
        summary = "Llega a estado terminal"
        explanation = (
            f"El estudiante sumo {move} y llego exactamente a {TARGET}. "
            "Ese es un estado terminal ganador: la partida termina porque se alcanzo la meta."
        )
    elif total_after % 4 == 2:
        summary = "Deja estado favorable"
        explanation = (
            f"El estudiante sumo {move} y llevo el contador a {total_after}. "
            "Este estado puede ser favorable porque en Carrera al 10 los multiplos y residuos alrededor de 4 ayudan a controlar la respuesta rival."
        )
    else:
        summary = "Abre respuestas para IA"
        explanation = (
            f"El estudiante sumo {move} y llevo el contador a {total_after}. "
            "La IA evaluara +1, +2 y +3 para buscar una ruta que le permita llegar a 10 antes que el estudiante."
        )
    return {
        "jugada": f"+{move}",
        "estado": str(total_after),
        "resumen": summary,
        "explicacion": explanation,
    }


def explain_ai_race_move(total_before: int, move: Optional[int], result: RaceResult) -> Dict[str, str]:
    if move is None:
        return {
            "jugada": "sin jugada",
            "estado": str(total_before),
            "utilidad": str(result.score),
            "nodos": str(result.nodes),
            "resumen": "Sin opciones",
            "explicacion": "La IA no tiene movimientos legales porque la partida ya alcanzo un estado terminal.",
        }

    total_after = total_before + move
    if total_after == TARGET:
        summary = "Gana llegando a 10"
        explanation = (
            f"La IA sumo {move} y alcanzo exactamente {TARGET}. "
            "Minimax detecto un estado terminal ganador y por eso selecciono esa accion."
        )
    elif result.score == 1:
        summary = "Construye ruta ganadora"
        explanation = (
            f"La IA sumo {move} y llevo el contador a {total_after}. "
            "Al explorar el arbol, encontro que esta rama puede conducir a victoria si responde de forma optima."
        )
    elif result.score == 0:
        summary = "Mantiene equilibrio"
        explanation = (
            f"La IA sumo {move} y llevo el contador a {total_after}. "
            "El valor 0 indica que la posicion no garantiza victoria inmediata, pero conserva equilibrio estrategico."
        )
    else:
        summary = "Reduce riesgo"
        explanation = (
            f"La IA sumo {move} y llevo el contador a {total_after}. "
            "El arbol indica riesgo de derrota ante una respuesta optima del estudiante; aun asi, eligio la mejor opcion disponible."
        )
    return {
        "jugada": f"+{move}",
        "estado": str(total_after),
        "utilidad": str(result.score),
        "nodos": str(result.nodes),
        "resumen": summary,
        "explicacion": explanation,
    }


def build_tree_rows(total: int, depth: int = 2) -> List[Dict[str, str]]:
    rows = []
    for ai_move in legal_moves(total):
        ai_total = total + ai_move
        ai_counter = {"nodes": 0}
        ai_score, _ = minimax_race(ai_total, False, ai_counter)
        rows.append(
            {
                "Nivel": "IA",
                "Ruta": f"{total} -> +{ai_move} -> {ai_total}",
                "Valor": str(ai_score),
                "Lectura": interpret_race_score(ai_score),
            }
        )
        if depth > 1 and not is_terminal(ai_total):
            for human_move in legal_moves(ai_total):
                human_total = ai_total + human_move
                human_counter = {"nodes": 0}
                score, _ = minimax_race(human_total, True, human_counter)
                rows.append(
                    {
                        "Nivel": "Estudiante",
                        "Ruta": f"{total} -> +{ai_move} -> {ai_total} -> +{human_move} -> {human_total}",
                        "Valor": str(score),
                        "Lectura": "Respuesta posible de MIN",
                    }
                )
    return rows


def race_progress(total: int) -> float:
    return min(1.0, total / TARGET)
