import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


EMPTY = " "
HUMAN = "O"
AI = "X"

WINNING_LINES: Tuple[Tuple[int, int, int], ...] = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


@dataclass
class SearchResult:
    score: int
    move: Optional[int]
    nodes: int
    pruned: int = 0


def empty_board() -> List[str]:
    return [EMPTY] * 9


def available_moves(board: List[str]) -> List[int]:
    return [index for index, cell in enumerate(board) if cell == EMPTY]


def check_winner(board: List[str]) -> Optional[str]:
    for a, b, c in WINNING_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    if EMPTY not in board:
        return "Draw"
    return None


def evaluate_terminal(result: Optional[str]) -> int:
    if result == AI:
        return 1
    if result == HUMAN:
        return -1
    return 0


def minimax(board: List[str], is_maximizing: bool, counter: Dict[str, int]) -> Tuple[int, Optional[int]]:
    counter["nodes"] += 1
    result = check_winner(board)
    if result is not None:
        return evaluate_terminal(result), None

    if is_maximizing:
        best_score = -math.inf
        best_move = None
        for move in available_moves(board):
            board[move] = AI
            score, _ = minimax(board, False, counter)
            board[move] = EMPTY
            if score > best_score:
                best_score = score
                best_move = move
        return int(best_score), best_move

    best_score = math.inf
    best_move = None
    for move in available_moves(board):
        board[move] = HUMAN
        score, _ = minimax(board, True, counter)
        board[move] = EMPTY
        if score < best_score:
            best_score = score
            best_move = move
    return int(best_score), best_move


def alphabeta(
    board: List[str],
    is_maximizing: bool,
    alpha: float,
    beta: float,
    counter: Dict[str, int],
) -> Tuple[int, Optional[int]]:
    counter["nodes"] += 1
    result = check_winner(board)
    if result is not None:
        return evaluate_terminal(result), None

    if is_maximizing:
        best_score = -math.inf
        best_move = None
        for move in available_moves(board):
            board[move] = AI
            score, _ = alphabeta(board, False, alpha, beta, counter)
            board[move] = EMPTY
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                counter["pruned"] += 1
                break
        return int(best_score), best_move

    best_score = math.inf
    best_move = None
    for move in available_moves(board):
        board[move] = HUMAN
        score, _ = alphabeta(board, True, alpha, beta, counter)
        board[move] = EMPTY
        if score < best_score:
            best_score = score
            best_move = move
        beta = min(beta, best_score)
        if beta <= alpha:
            counter["pruned"] += 1
            break
    return int(best_score), best_move


def run_minimax(board: List[str]) -> SearchResult:
    counter = {"nodes": 0, "pruned": 0}
    score, move = minimax(board.copy(), True, counter)
    return SearchResult(score=score, move=move, nodes=counter["nodes"], pruned=0)


def run_alphabeta(board: List[str]) -> SearchResult:
    counter = {"nodes": 0, "pruned": 0}
    score, move = alphabeta(board.copy(), True, -math.inf, math.inf, counter)
    return SearchResult(score=score, move=move, nodes=counter["nodes"], pruned=counter["pruned"])


def get_recommendations(board: List[str]) -> Dict[str, SearchResult]:
    return {
        "Minimax": run_minimax(board),
        "Alfa-Beta": run_alphabeta(board),
    }


def evaluate_ai_moves(board: List[str]) -> List[Dict[str, str]]:
    return evaluate_all_ai_options(board, "Minimax")


def interpret_score(score: int, board_after_ai_move: Optional[List[str]] = None) -> str:
    if score == 1:
        return "Puede llevar a victoria"
    if score == 0:
        return "Puede llevar a empate"
    if board_after_ai_move and creates_immediate_threat(board_after_ai_move, HUMAN):
        return "Puede permitir victoria del adversario"
    return "Riesgosa"


def creates_immediate_threat(board: List[str], player: str) -> bool:
    return bool(detect_threats(board, player))


def detect_threats(board: List[str], player: str) -> List[Dict[str, str]]:
    threats = []
    for line in WINNING_LINES:
        values = [board[index] for index in line]
        if values.count(player) == 2 and values.count(EMPTY) == 1:
            empty_index = line[values.index(EMPTY)]
            threats.append(
                {
                    "linea": "-".join(str(index + 1) for index in line),
                    "posicion_bloqueo": str(empty_index + 1),
                }
            )
    return threats


def immediate_winning_moves(board: List[str], player: str) -> List[int]:
    winning_moves = []
    for move in available_moves(board):
        candidate = board.copy()
        candidate[move] = player
        if check_winner(candidate) == player:
            winning_moves.append(move)
    return winning_moves


def move_style(move: Optional[int]) -> str:
    if move == 4:
        return "centro"
    if move in (0, 2, 6, 8):
        return "esquina"
    if move in (1, 3, 5, 7):
        return "lateral"
    return "sin posicion"


def explain_student_move(board_before: List[str], board_after: List[str], move: int) -> Dict[str, str]:
    style = move_style(move)
    created = detect_threats(board_after, HUMAN)
    blocked = move in immediate_winning_moves(board_before, AI)
    ai_opportunity = bool(immediate_winning_moves(board_after, AI))

    if style == "centro":
        core = "Esta es una jugada fuerte porque controla el centro del tablero."
        pedagogy = "Dicho facil: desde el centro puedes formar lineas hacia muchos lados, asi que obligas a la IA a vigilar mas amenazas."
        short = "Controla el centro"
    elif style == "esquina":
        core = "Esta jugada ocupa una esquina, una posicion valiosa para construir diagonales."
        pedagogy = "Dicho facil: una esquina puede conectarse con una fila, una columna y una diagonal."
        short = "Activa una esquina"
    else:
        core = "Esta jugada ocupa un lateral. Puede ser util, aunque suele ser menos flexible que centro o esquina."
        pedagogy = "Dicho facil: sirve para bloquear o preparar una linea, pero normalmente da menos caminos de ataque."
        short = "Usa un lateral"

    details = [f"El estudiante jugo en la posicion {move + 1}.", core, pedagogy]
    if created:
        details.append("Ademas, creo una amenaza: si la IA no la bloquea, podrias ganar en tu proximo turno.")
        short = "Crea una amenaza"
    if blocked:
        details.append("Tambien bloqueaste una amenaza inmediata de la IA. En palabras simples: cerraste una puerta por donde X podia ganar.")
        short = "Bloquea amenaza"
    if ai_opportunity:
        details.append("Cuidado: el tablero deja una oportunidad para que la IA complete tres en linea ahora mismo.")
        short = "Deja oportunidad a la IA"

    return {
        "posicion": str(move + 1),
        "estado_tablero": board_to_text(board_after),
        "creo_amenaza": "Si" if created else "No",
        "bloqueo_amenaza": "Si" if blocked else "No",
        "dejo_oportunidad_ia": "Si" if ai_opportunity else "No",
        "explicacion": " ".join(details),
        "resumen": short,
    }


def explain_ai_move(
    board_before: List[str],
    board_after: List[str],
    move: Optional[int],
    strategy: str,
    score: int,
    nodes: int,
    pruned: int,
    minimax_nodes: int = 0,
) -> Dict[str, str]:
    if move is None:
        return {
            "estrategia": strategy,
            "jugada": "sin jugada",
            "utilidad": str(score),
            "nodos": str(nodes),
            "ramas_podadas": str(pruned),
            "explicacion": "La IA no encontro jugadas disponibles porque el tablero ya esta cerrado.",
            "resumen": "Sin jugadas",
        }

    blocked = move in immediate_winning_moves(board_before, HUMAN)
    completed_win = check_winner(board_after) == AI
    saving = exploration_saving(minimax_nodes, nodes) if strategy == "Alfa-Beta" else 0.0

    reasons = [
        f"La IA eligio la posicion {move + 1} usando {strategy}.",
        f"El puntaje de esa jugada fue {score}: 1 significa que favorece a la IA, 0 que apunta a empate y -1 que favorece al estudiante.",
        "En palabras simples, la IA no mira solo donde poner X ahora; tambien imagina que haras tu despues y elige el camino mas seguro.",
    ]
    summary = "Maximiza utilidad"

    if completed_win:
        reasons.append("La jugada completa tres en linea. Eso significa que encontro un final ganador y no necesita seguir imaginando mas jugadas.")
        summary = "Completa victoria"
    elif blocked:
        reasons.append("La jugada bloquea una amenaza inmediata del estudiante. Si no lo hacia, O podia ganar en el siguiente turno.")
        summary = "Bloquea amenaza"
    elif score == 1:
        reasons.append("Al revisar los caminos posibles, la IA encontro que esta opcion puede llevarla a ganar si continua jugando bien.")
        summary = "Busca victoria"
    elif score == 0:
        reasons.append("La IA no vio una victoria segura, asi que eligio una opcion que protege el empate y evita perder.")
        summary = "Fuerza empate"
    else:
        reasons.append("La posicion es dificil para la IA. Esta jugada no garantiza ganar, pero reduce el dano frente a tus posibles respuestas.")
        summary = "Reduce perdida"

    if strategy == "Alfa-Beta":
        reasons.append(
            f"Con Alfa-Beta reviso {nodes} situaciones y corto {pruned} caminos que ya no servian. Eso ahorro aproximadamente {saving}% de revision frente a Minimax."
        )

    return {
        "estrategia": strategy,
        "jugada": str(move + 1),
        "utilidad": str(score),
        "nodos": str(nodes),
        "ramas_podadas": str(pruned),
        "explicacion": " ".join(reasons),
        "resumen": summary,
    }


def evaluate_all_ai_options(board: List[str], strategy: str = "Minimax") -> List[Dict[str, str]]:
    rows = []
    human_wins = set(immediate_winning_moves(board, HUMAN))
    for move in available_moves(board):
        candidate = board.copy()
        candidate[move] = AI
        counter = {"nodes": 0, "pruned": 0}
        if strategy == "Alfa-Beta":
            score, _ = alphabeta(candidate, False, -math.inf, math.inf, counter)
        else:
            score, _ = minimax(candidate, False, counter)

        if check_winner(candidate) == AI:
            expected = "Victoria posible para IA"
            interpretation = "La IA gana de inmediato porque completa tres en linea."
        elif move in human_wins:
            expected = "Bloqueo necesario"
            interpretation = "La IA debe jugar aqui para impedir que el estudiante gane enseguida."
        elif score == 1:
            expected = "Victoria posible para IA"
            interpretation = "Si ambos juegan bien, este camino favorece a la IA."
        elif score == 0:
            expected = "Empate probable"
            interpretation = "Este camino no asegura victoria, pero mantiene la partida controlada."
        else:
            expected = "Riesgo de derrota"
            interpretation = "El estudiante podria aprovechar este camino para acercarse a ganar."

        rows.append(
            {
                "Posicion posible": str(move + 1),
                "Valor Minimax": str(score),
                "Resultado esperado": expected,
                "Interpretacion pedagogica": interpretation,
            }
        )
    return rows


def get_learning_concept(turn_number: int, strategy: str) -> Dict[str, str]:
    concepts = [
        {
            "concepto": "Arbol de juego",
            "explicacion": "Un arbol de juego es como un mapa de futuros posibles: si juego aqui, luego tu puedes responder alla.",
        },
        {
            "concepto": "Jugador MAX",
            "explicacion": "MAX es la IA intentando conseguir el mejor resultado para X.",
        },
        {
            "concepto": "Jugador MIN",
            "explicacion": "MIN eres tu desde la mirada de la IA: tus jugadas pueden bloquearla o hacerla perder.",
        },
        {
            "concepto": "Funcion de utilidad",
            "explicacion": "La funcion de utilidad es una tabla de puntajes: ganar vale 1, empatar vale 0 y perder vale -1.",
        },
        {
            "concepto": "Estado terminal",
            "explicacion": "Un estado terminal es cuando la partida ya termino: alguien gano o hubo empate.",
        },
        {
            "concepto": "Complejidad",
            "explicacion": "Complejidad significa cantidad de trabajo: mientras mas casillas libres, mas futuros debe revisar la IA.",
        },
        {
            "concepto": "Poda",
            "explicacion": "Podar es dejar de revisar un camino cuando ya sabes que no sera la mejor opcion.",
        },
        {
            "concepto": "Heuristica",
            "explicacion": "Una heuristica es una regla practica, como preferir centro o esquinas cuando no puedes calcularlo todo.",
        },
        {
            "concepto": "Informacion perfecta",
            "explicacion": "En Tres en Raya ambos jugadores ven todo el tablero; no hay cartas ni acciones ocultas.",
        },
    ]
    if strategy == "Alfa-Beta":
        return concepts[6]
    return concepts[(max(1, turn_number) - 1) % len(concepts)]


def board_to_text(board: List[str]) -> str:
    values = [cell if cell != EMPTY else "-" for cell in board]
    return f"{values[0]} {values[1]} {values[2]} / {values[3]} {values[4]} {values[5]} / {values[6]} {values[7]} {values[8]}"


def move_label(move: Optional[int]) -> str:
    return "sin jugada" if move is None else f"posicion {move + 1}"


def explain_agent_thought(
    board_before: List[str],
    board_after: List[str],
    strategy: str,
    result: SearchResult,
    comparison: Dict[str, SearchResult],
) -> List[str]:
    thoughts = [f"La IA actuo como jugador MAX y eligio {move_label(result.move)} con valor {result.score}."]
    if result.score == 1:
        thoughts.append("Esta buscando una linea que garantice victoria si el adversario responde de forma optima.")
    elif result.score == 0:
        thoughts.append("Esta forzando un empate, que es el mejor resultado disponible ante defensa optima.")
    else:
        thoughts.append("Esta reduciendo el dano: todas las rutas son desfavorables si el rival juega bien.")

    if creates_immediate_threat(board_before, HUMAN):
        thoughts.append("Tambien reviso amenazas inmediatas del estudiante para bloquear una posible victoria.")

    if check_winner(board_after) == AI:
        thoughts.append("La jugada completa una linea ganadora para la IA.")

    if strategy == "Alfa-Beta":
        mm_nodes = comparison["Minimax"].nodes
        ab_nodes = comparison["Alfa-Beta"].nodes
        saving = exploration_saving(mm_nodes, ab_nodes)
        thoughts.append(f"Uso poda alfa-beta y redujo la exploracion en aproximadamente {saving}%.")

    return thoughts


def exploration_saving(minimax_nodes: int, alphabeta_nodes: int) -> float:
    if minimax_nodes <= 0:
        return 0.0
    return round(max(0.0, (1 - alphabeta_nodes / minimax_nodes) * 100), 2)
