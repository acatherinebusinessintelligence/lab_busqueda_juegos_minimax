import streamlit as st

from game_logic import (
    AI,
    EMPTY,
    HUMAN,
    board_to_text,
    check_winner,
    detect_threats,
    empty_board,
    evaluate_all_ai_options,
    explain_ai_move,
    explain_student_move,
    exploration_saving,
    get_learning_concept,
    get_recommendations,
    move_label,
)
from quiz_data import CONCEPTS, QUIZ_QUESTIONS
from utils import (
    append_student_response,
    build_evidence_markdown,
    general_feedback,
    now_label,
    performance_level,
    slugify_name,
)


st.set_page_config(
    page_title="OVA Unidad 3: Busqueda en juegos",
    page_icon="🎮",
    layout="wide",
)


SECTIONS = [
    "Inicio",
    "Conceptos clave",
    "Laboratorio interactivo",
    "Comparacion Minimax vs Alfa-Beta",
    "Juegos con informacion imperfecta",
    "Juegos en tiempo real",
    "Quiz formativo",
    "Evidencia y retroalimentacion final",
]


def init_state() -> None:
    defaults = {
        "student": {"name": "", "student_id": "", "group": "", "email": ""},
        "board": empty_board(),
        "game_over": False,
        "message": "Tu turno. Juegas con O. La IA juega con X.",
        "last_human_move": None,
        "last_ai_move": None,
        "last_ai_score": None,
        "last_student_analysis": None,
        "last_ai_analysis": None,
        "last_ai_options": [],
        "learning_concept": None,
        "move_history": [],
        "game_result": "Partida en curso",
        "show_lab_comparison": False,
        "strategy_used": "Minimax",
        "max_minimax_nodes": 0,
        "max_alphabeta_nodes": 0,
        "max_pruned": 0,
        "real_time_reflection": "",
        "final_reflection": "",
        "quiz_answers": {},
        "quiz_submitted": False,
        "quiz_score": 0,
        "quiz_percentage": 0.0,
        "csv_saved": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        .main .block-container {padding-top: 2rem; max-width: 1180px;}
        h1, h2, h3 {letter-spacing: 0;}
        .hero {
            border-left: 6px solid #2f6f6d;
            background: linear-gradient(135deg, #f7fbfa 0%, #eef5f1 52%, #f8f4ed 100%);
            padding: 1.4rem 1.6rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        .card {
            border: 1px solid #d9e2df;
            background: #ffffff;
            border-radius: 8px;
            padding: 1rem;
            min-height: 150px;
            box-shadow: 0 1px 5px rgba(35, 54, 53, 0.06);
        }
        .metric-card {
            border: 1px solid #d8ddd8;
            border-radius: 8px;
            padding: .8rem;
            background: #fbfcfb;
        }
        .board button {
            height: 112px;
            font-size: 2.8rem !important;
            font-weight: 700 !important;
            border: 1px solid #9bb8b2 !important;
            background: #fbfdfc !important;
        }
        .board-wrap {max-width: 520px; margin: 0 auto;}
        .turn-panel {
            border: 1px solid #d9e2df;
            border-radius: 8px;
            padding: 1rem;
            background: #ffffff;
            margin-bottom: .8rem;
        }
        .small-note {color: #51615f; font-size: .93rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def student_is_registered() -> bool:
    student = st.session_state.student
    return all(student.get(field, "").strip() for field in ("name", "student_id", "group", "email"))


def render_student_registration() -> None:
    st.sidebar.markdown("### Registro del estudiante")
    with st.sidebar.form("student_registration"):
        name = st.text_input("Nombre completo", value=st.session_state.student["name"])
        student_id = st.text_input("Codigo o identificacion", value=st.session_state.student["student_id"])
        group = st.text_input("Grupo o curso", value=st.session_state.student["group"])
        email = st.text_input("Correo institucional", value=st.session_state.student["email"])
        saved = st.form_submit_button("Guardar registro", use_container_width=True)
        if saved:
            st.session_state.student = {
                "name": name.strip(),
                "student_id": student_id.strip(),
                "group": group.strip(),
                "email": email.strip(),
            }
            if student_is_registered():
                st.sidebar.success("Registro completo.")
            else:
                st.sidebar.warning("Completa todos los campos para avanzar.")


def require_registration(section: str) -> bool:
    if section == "Inicio" or student_is_registered():
        return True
    st.warning("Para avanzar al laboratorio debes completar el registro del estudiante en la barra lateral.")
    return False


def render_learning_cards() -> None:
    st.markdown("## ¿Que vas a aprender en este modulo?")
    cards = [
        ("1", "Como piensa un agente en un juego competitivo.", "Anticipa tus respuestas, evalua consecuencias y decide con una meta."),
        ("2", "Como funciona el algoritmo Minimax.", "Alterna turnos MAX/MIN para escoger el mejor resultado posible."),
        ("3", "Como la poda Alfa-Beta mejora la eficiencia.", "Evita explorar ramas que no pueden cambiar la decision final."),
        ("4", "Que cambia con informacion imperfecta o tiempo real.", "Aparecen incertidumbre, limites de profundidad y heuristicas."),
    ]
    cols = st.columns(4)
    for col, (number, title, body) in zip(cols, cards):
        with col:
            st.markdown(f"<div class='card'><b>{number}. {title}</b><p>{body}</p></div>", unsafe_allow_html=True)


def render_home() -> None:
    st.markdown(
        """
        <div class='hero'>
        <h1>Jugadas Inteligentes: Estrategias Optimas en Juegos a traves de la Busqueda</h1>
        <p><b>Unidad 3:</b> Busqueda en juegos y agentes adversarios.</p>
        <p><b>Resultado de aprendizaje:</b> El estudiante analiza y aplica algoritmos de busqueda en juegos, considerando complejidad, eficiencia y optimizacion.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write(
        "Este OVA convierte el Tres en Raya en un laboratorio de decision adversarial. "
        "Vas a jugar contra una IA, observar nodos explorados, comparar Minimax con Alfa-Beta, "
        "resolver preguntas formativas y generar una evidencia descargable."
    )
    st.info(
        "Navega desde el menu lateral. Completa primero el registro del estudiante; despues podras avanzar por conceptos, laboratorio, quiz y evidencia final."
    )
    render_learning_cards()


def render_concepts() -> None:
    st.title("Conceptos clave")
    st.write("Cada concepto conecta la teoria con una decision concreta en Tres en Raya.")
    for index, concept in enumerate(CONCEPTS):
        with st.expander(concept["title"], expanded=index < 2):
            st.markdown(f"**Definicion breve:** {concept['definition']}")
            st.markdown(f"**Ejemplo aplicado:** {concept['example']}")
            answer = st.radio(
                concept["question"],
                concept["options"],
                key=f"concept_{index}",
                index=None,
            )
            if answer:
                if answer == concept["answer"]:
                    st.success(concept["feedback"])
                else:
                    st.error(f"Revisa la idea central. {concept['feedback']}")


def reset_game() -> None:
    st.session_state.board = empty_board()
    st.session_state.game_over = False
    st.session_state.message = "Tu turno. Juegas con O. La IA juega con X."
    st.session_state.last_human_move = None
    st.session_state.last_ai_move = None
    st.session_state.last_ai_score = None
    st.session_state.last_student_analysis = None
    st.session_state.last_ai_analysis = None
    st.session_state.last_ai_options = []
    st.session_state.learning_concept = None
    st.session_state.move_history = []
    st.session_state.game_result = "Partida en curso"
    st.session_state.show_lab_comparison = False


def update_max_metrics(recommendations) -> None:
    st.session_state.max_minimax_nodes = max(
        st.session_state.max_minimax_nodes,
        recommendations["Minimax"].nodes,
    )
    st.session_state.max_alphabeta_nodes = max(
        st.session_state.max_alphabeta_nodes,
        recommendations["Alfa-Beta"].nodes,
    )
    st.session_state.max_pruned = max(
        st.session_state.max_pruned,
        recommendations["Alfa-Beta"].pruned,
    )


def add_history(player: str, move, summary: str, explanation: str) -> None:
    st.session_state.move_history.append(
        {
            "Turno": len(st.session_state.move_history) + 1,
            "Jugador": player,
            "Posicion": "-" if move is None else str(move + 1),
            "Explicacion breve": summary,
            "Explicacion completa": explanation,
        }
    )


def finish_game_message(winner: str) -> None:
    st.session_state.game_over = True
    if winner == AI:
        st.session_state.game_result = "Gano la IA"
        st.session_state.message = "La IA gano. Observa que linea logro construir o forzar."
    elif winner == HUMAN:
        st.session_state.game_result = "Gano el estudiante"
        st.session_state.message = "Ganaste. Excelente lectura del tablero."
    else:
        st.session_state.game_result = "Empate"
        st.session_state.message = "Empate. Ambos jugadores evitaron una derrota."


def ai_play(strategy: str) -> None:
    board_before = st.session_state.board.copy()
    recommendations = get_recommendations(board_before)
    update_max_metrics(recommendations)
    result = recommendations[strategy]
    st.session_state.last_ai_options = evaluate_all_ai_options(board_before, strategy)
    if result.move is not None:
        st.session_state.board[result.move] = AI
    st.session_state.last_ai_move = result.move
    st.session_state.last_ai_score = result.score
    st.session_state.strategy_used = strategy
    st.session_state.last_ai_analysis = explain_ai_move(
        board_before,
        st.session_state.board.copy(),
        result.move,
        strategy,
        result.score,
        result.nodes,
        result.pruned,
        recommendations["Minimax"].nodes,
    )
    add_history(
        "IA",
        result.move,
        st.session_state.last_ai_analysis["resumen"],
        st.session_state.last_ai_analysis["explicacion"],
    )
    st.session_state.learning_concept = get_learning_concept(len(st.session_state.move_history), strategy)

    winner = check_winner(st.session_state.board)
    if winner:
        finish_game_message(winner)
    else:
        st.session_state.message = f"La IA jugo con {strategy}. Ahora vuelve tu turno."


def render_board(strategy: str) -> None:
    st.markdown("<div class='board-wrap'><div class='board'>", unsafe_allow_html=True)
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            index = row * 3 + col
            label = st.session_state.board[index] if st.session_state.board[index] != EMPTY else " "
            disabled = st.session_state.game_over or st.session_state.board[index] != EMPTY
            if cols[col].button(label, key=f"cell_{index}", use_container_width=True, disabled=disabled):
                board_before = st.session_state.board.copy()
                st.session_state.board[index] = HUMAN
                st.session_state.last_human_move = index
                board_after = st.session_state.board.copy()
                st.session_state.last_student_analysis = explain_student_move(board_before, board_after, index)
                add_history(
                    "Estudiante",
                    index,
                    st.session_state.last_student_analysis["resumen"],
                    st.session_state.last_student_analysis["explicacion"],
                )
                st.session_state.learning_concept = get_learning_concept(len(st.session_state.move_history), strategy)
                winner = check_winner(st.session_state.board)
                if winner:
                    finish_game_message(winner)
                else:
                    ai_play(strategy)
                st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)


def render_lab() -> None:
    st.title("Laboratorio interactivo: Tres en Raya")
    st.info(
        "En este laboratorio jugaras Tres en Raya contra un agente inteligente. Tu seras el jugador O y la IA sera el jugador X. "
        "La IA usara Minimax o Poda Alfa-Beta para decidir su jugada. Despues de cada movimiento, el sistema explicara como evaluo el agente el tablero y por que eligio su accion."
    )
    strategy = st.radio("Estrategia de la IA", ["Minimax", "Alfa-Beta"], horizontal=True, key="lab_strategy")
    st.session_state.strategy_used = strategy

    recommendations = get_recommendations(st.session_state.board.copy())
    update_max_metrics(recommendations)
    mm = recommendations["Minimax"]
    ab = recommendations["Alfa-Beta"]
    saving = exploration_saving(mm.nodes, ab.nodes)

    st.caption("Posiciones: 1-2-3 arriba, 4-5-6 al centro, 7-8-9 abajo.")

    left, right = st.columns([1.05, 1.15])
    with left:
        st.subheader("Tablero de juego")
        render_board(strategy)
        st.info(st.session_state.message)
        controls = st.columns(2)
        if controls[0].button("Reiniciar juego", use_container_width=True):
            reset_game()
            st.rerun()
        controls[1].metric("Resultado", st.session_state.game_result)

    with right:
        st.subheader("Estado y metricas")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Nodos Minimax", mm.nodes)
        m2.metric("Nodos Alfa-Beta", ab.nodes)
        m3.metric("Ramas podadas", ab.pruned)
        m4.metric("Ahorro", f"{saving}%")
        st.write(f"**Tablero actual:** {board_to_text(st.session_state.board)}")

        if st.button("Comparar algoritmos en este tablero", use_container_width=True):
            st.session_state.show_lab_comparison = True

        if st.session_state.get("show_lab_comparison"):
            st.markdown("### Comparacion en este tablero")
            st.write(f"**Mejor jugada segun Minimax:** {move_label(mm.move)}")
            st.write(f"**Mejor jugada segun Alfa-Beta:** {move_label(ab.move)}")
            st.write(f"**Nodos explorados por Minimax:** {mm.nodes}")
            st.write(f"**Nodos explorados por Alfa-Beta:** {ab.nodes}")
            st.write(f"**Ramas podadas:** {ab.pruned}")
            st.write(f"**Ahorro porcentual:** {saving}%")
            st.success(
                "Ambos algoritmos pueden llegar a la misma decision, pero Alfa-Beta evita explorar ramas que no cambiarian el resultado final. Por eso es mas eficiente."
            )

    st.divider()
    analysis_cols = st.columns(2)
    with analysis_cols[0]:
        st.subheader("Analisis del movimiento del estudiante")
        analysis = st.session_state.last_student_analysis
        if analysis:
            st.markdown(
                f"""
                <div class='turn-panel'>
                <b>Posicion elegida:</b> {analysis['posicion']}<br>
                <b>Estado actual del tablero:</b> {analysis['estado_tablero']}<br>
                <b>Creo amenaza:</b> {analysis['creo_amenaza']}<br>
                <b>Bloqueo amenaza:</b> {analysis['bloqueo_amenaza']}<br>
                <b>Dejo oportunidad para la IA:</b> {analysis['dejo_oportunidad_ia']}
                <p>{analysis['explicacion']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.caption("Haz clic en una casilla para recibir retroalimentacion inmediata.")

    with analysis_cols[1]:
        st.subheader("Pensamiento del agente")
        ai_analysis = st.session_state.last_ai_analysis
        if ai_analysis:
            st.markdown(
                f"""
                <div class='turn-panel'>
                <b>Estrategia usada:</b> {ai_analysis['estrategia']}<br>
                <b>Jugada seleccionada:</b> {ai_analysis['jugada']}<br>
                <b>Valor de utilidad estimado:</b> {ai_analysis['utilidad']}<br>
                <b>Nodos explorados:</b> {ai_analysis['nodos']}<br>
                <b>Ramas podadas:</b> {ai_analysis['ramas_podadas']}
                <p>{ai_analysis['explicacion']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.caption("La IA respondera automaticamente despues de tu primera jugada.")

    st.subheader("Opciones evaluadas por la IA")
    rows = st.session_state.last_ai_options or evaluate_all_ai_options(st.session_state.board.copy(), strategy)
    if rows:
        st.table(rows)
    else:
        st.write("No hay jugadas disponibles en este estado.")

    st.subheader("Lo que acabas de aprender")
    concept = st.session_state.learning_concept
    if concept:
        st.success(f"Concepto aplicado: {concept['concepto']}. {concept['explicacion']}")
    else:
        st.info("El primer concepto aparecera despues de tu movimiento inicial.")

    st.subheader("Historial de jugadas")
    if st.session_state.move_history:
        st.table(
            [
                {
                    "Turno": item["Turno"],
                    "Jugador": item["Jugador"],
                    "Posicion": item["Posicion"],
                    "Explicacion breve": item["Explicacion breve"],
                }
                for item in st.session_state.move_history
            ]
        )
    else:
        st.caption("Aun no hay jugadas registradas.")


def render_comparison() -> None:
    st.title("Comparacion Minimax vs Alfa-Beta")
    st.write(
        "Minimax explora el arbol de juego suponiendo que MAX y MIN juegan de forma optima. "
        "Alfa-Beta conserva esa decision, pero descarta ramas que ya no pueden mejorar el resultado."
    )
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Minimax")
        st.write("Ventaja: es claro y garantiza la decision optima en juegos pequenos de informacion perfecta.")
        st.write("Limitacion: el numero de nodos crece rapidamente con la profundidad y el factor de ramificacion.")
    with col2:
        st.markdown("### Poda Alfa-Beta")
        st.write("Ventaja: reduce exploracion sin cambiar el resultado de Minimax si se aplica correctamente.")
        st.write("Limitacion: su eficiencia depende del orden en que se evaluan las jugadas.")

    st.table(
        [
            {"Criterio": "Decision", "Minimax": "Optima", "Alfa-Beta": "Optima"},
            {"Criterio": "Exploracion", "Minimax": "Exhaustiva", "Alfa-Beta": "Selectiva con podas"},
            {"Criterio": "Costo", "Minimax": "Mayor", "Alfa-Beta": "Menor o igual"},
            {"Criterio": "Uso ideal", "Minimax": "Arboles pequenos", "Alfa-Beta": "Arboles mas grandes con buen ordenamiento"},
        ]
    )

    board = st.session_state.board if "board" in st.session_state else empty_board()
    recommendations = get_recommendations(board.copy())
    mm_nodes = recommendations["Minimax"].nodes
    ab_nodes = recommendations["Alfa-Beta"].nodes
    st.info(f"Ejemplo numerico con el tablero actual: Minimax explora {mm_nodes} nodos y Alfa-Beta explora {ab_nodes} nodos.")

    st.bar_chart(
        {
            "Minimax": [mm_nodes],
            "Alfa-Beta": [ab_nodes],
        },
        use_container_width=True,
    )


def render_imperfect_information() -> None:
    st.title("Juegos con informacion imperfecta")
    st.write("La informacion disponible cambia radicalmente la forma de decidir.")
    st.table(
        [
            {"Juego": "Ajedrez", "Tipo": "Informacion perfecta", "Razon": "Ambos jugadores ven todas las piezas."},
            {"Juego": "Poker", "Tipo": "Informacion imperfecta", "Razon": "Hay cartas privadas y probabilidades."},
            {"Juego": "Tres en Raya", "Tipo": "Informacion perfecta", "Razon": "Todo el tablero es visible."},
            {"Juego": "Piedra, papel o tijera simultaneo", "Tipo": "Incertidumbre estrategica", "Razon": "La accion rival no se observa antes de decidir."},
        ]
    )
    answer = st.radio(
        "¿El Tres en Raya es un juego de informacion perfecta o imperfecta?",
        [
            "A. Perfecta, porque ambos jugadores ven todo el tablero.",
            "B. Imperfecta, porque no se conocen las cartas del rival.",
            "C. Aleatoria, porque no hay reglas.",
            "D. En tiempo real, porque se juega rapido.",
        ],
        key="imperfect_activity",
        index=None,
    )
    if answer:
        if answer.startswith("A."):
            st.success("Correcto. Ambos jugadores observan el mismo tablero y las mismas acciones pasadas.")
        else:
            st.error("Revisa la definicion: en Tres en Raya no hay informacion oculta.")


def render_real_time() -> None:
    st.title("Juegos en tiempo real")
    st.write(
        "En juegos y sistemas en tiempo real, el agente no siempre puede explorar todo el arbol. "
        "Debe limitar profundidad, usar heuristicas y decidir bajo restricciones de tiempo."
    )
    st.markdown(
        """
        - **Profundidad limitada:** el agente mira solo algunos turnos hacia adelante.
        - **Heuristica:** estima que tan prometedor es un estado no terminal.
        - **Restriccion de tiempo:** obliga a balancear calidad de decision y velocidad.
        """
    )
    reflection = st.text_area(
        "Elige un videojuego, simulador, sistema de ciberseguridad, negociacion o situacion empresarial donde una IA deba decidir rapidamente. Explica que informacion tendria disponible, que no sabria y que criterio usaria para tomar decisiones.",
        value=st.session_state.real_time_reflection,
        height=180,
    )
    st.session_state.real_time_reflection = reflection


def render_quiz() -> None:
    st.title("Quiz formativo")
    st.write("Responde las preguntas y revisa la retroalimentacion automatica.")
    for index, item in enumerate(QUIZ_QUESTIONS):
        answer = st.radio(
            f"{index + 1}. {item['question']}",
            item["options"],
            key=f"quiz_{index}",
            index=None,
        )
        if answer:
            st.session_state.quiz_answers[index] = answer
            if answer == item["answer"]:
                st.success(item["feedback"])
            else:
                st.error(f"Respuesta incorrecta. {item['feedback']}")

    if st.button("Calcular resultado del quiz", type="primary"):
        score = sum(
            1 for index, item in enumerate(QUIZ_QUESTIONS) if st.session_state.quiz_answers.get(index) == item["answer"]
        )
        percentage = round(score / len(QUIZ_QUESTIONS) * 100, 2)
        st.session_state.quiz_score = score
        st.session_state.quiz_percentage = percentage
        st.session_state.quiz_submitted = True
        st.session_state.csv_saved = False
        st.rerun()

    if st.session_state.quiz_submitted:
        level = performance_level(st.session_state.quiz_percentage)
        st.subheader("Resultado")
        c1, c2, c3 = st.columns(3)
        c1.metric("Puntaje", f"{st.session_state.quiz_score}/{len(QUIZ_QUESTIONS)}")
        c2.metric("Porcentaje", f"{st.session_state.quiz_percentage}%")
        c3.metric("Nivel", level)
        st.info(general_feedback(level))


def evidence_data() -> dict:
    level = performance_level(st.session_state.quiz_percentage)
    comparison = (
        f"Minimax observo hasta {st.session_state.max_minimax_nodes} nodos; "
        f"Alfa-Beta observo hasta {st.session_state.max_alphabeta_nodes} nodos y podo hasta {st.session_state.max_pruned} ramas."
    )
    history_lines = []
    for item in st.session_state.move_history:
        history_lines.append(
            f"- Turno {item['Turno']} | {item['Jugador']} | Posicion {item['Posicion']} | {item['Explicacion breve']}: {item['Explicacion completa']}"
        )
    quiz_lines = []
    for index, item in enumerate(QUIZ_QUESTIONS):
        answer = st.session_state.quiz_answers.get(index, "Sin responder")
        quiz_lines.append(f"- {index + 1}. {item['question']} Respuesta: {answer}. Correcta: {item['answer']}.")
    return {
        "timestamp": now_label(),
        "name": st.session_state.student["name"],
        "student_id": st.session_state.student["student_id"],
        "group": st.session_state.student["group"],
        "email": st.session_state.student["email"],
        "quiz_score": str(st.session_state.quiz_score),
        "quiz_total": str(len(QUIZ_QUESTIONS)),
        "quiz_percentage": str(st.session_state.quiz_percentage),
        "level": level,
        "feedback": general_feedback(level),
        "real_time_reflection": st.session_state.real_time_reflection or "Sin respuesta registrada.",
        "final_reflection": st.session_state.final_reflection or "Sin respuesta registrada.",
        "strategy": st.session_state.strategy_used,
        "minimax_nodes": str(st.session_state.max_minimax_nodes),
        "alphabeta_nodes": str(st.session_state.max_alphabeta_nodes),
        "pruned": str(st.session_state.max_pruned),
        "comparison": comparison,
        "game_result": st.session_state.game_result,
        "move_history": "\n".join(history_lines) if history_lines else "Sin jugadas registradas.",
        "quiz_answers": "\n".join(quiz_lines) if quiz_lines else "Sin respuestas registradas.",
        "lessons": "Un agente adversarial decide anticipando respuestas del oponente, valorando resultados y optimizando la exploracion.",
    }


def render_evidence() -> None:
    st.title("Evidencia y retroalimentacion final")
    student = st.session_state.student
    st.subheader("Datos del estudiante")
    st.table(
        [
            {"Campo": "Nombre", "Valor": student["name"]},
            {"Campo": "Codigo", "Valor": student["student_id"]},
            {"Campo": "Grupo", "Valor": student["group"]},
            {"Campo": "Correo", "Valor": student["email"]},
        ]
    )

    st.subheader("Desempeno")
    level = performance_level(st.session_state.quiz_percentage)
    c1, c2, c3 = st.columns(3)
    c1.metric("Quiz", f"{st.session_state.quiz_score}/{len(QUIZ_QUESTIONS)}")
    c2.metric("Porcentaje", f"{st.session_state.quiz_percentage}%")
    c3.metric("Nivel", level)
    st.write(general_feedback(level))
    st.write(
        f"Estrategia usada en laboratorio: **{st.session_state.strategy_used}**. "
        f"Nodos maximos observados: Minimax {st.session_state.max_minimax_nodes}, "
        f"Alfa-Beta {st.session_state.max_alphabeta_nodes}, ramas podadas {st.session_state.max_pruned}."
    )
    st.write(f"Resultado de la partida: **{st.session_state.game_result}**.")
    if st.session_state.move_history:
        st.subheader("Historial registrado")
        st.table(
            [
                {
                    "Turno": item["Turno"],
                    "Jugador": item["Jugador"],
                    "Posicion": item["Posicion"],
                    "Explicacion breve": item["Explicacion breve"],
                }
                for item in st.session_state.move_history
            ]
        )
    st.write("Leccion aprendida: un agente inteligente decide anticipando adversarios, evaluando utilidad y optimizando exploracion.")

    final_reflection = st.text_area(
        "Reflexion final del estudiante: ¿Que aprendiste sobre la forma en que un agente inteligente toma decisiones frente a un adversario?",
        value=st.session_state.final_reflection,
        height=160,
    )
    st.session_state.final_reflection = final_reflection

    data = evidence_data()
    markdown = build_evidence_markdown(data)
    filename = f"evidencia_unidad3_{slugify_name(student['name'])}.md"
    st.download_button(
        "Descargar evidencia en Markdown",
        data=markdown,
        file_name=filename,
        mime="text/markdown",
        use_container_width=True,
    )

    if st.button("Guardar respuestas en CSV local", use_container_width=True):
        append_student_response(
            {
                "fecha_hora": data["timestamp"],
                "nombre": data["name"],
                "codigo": data["student_id"],
                "grupo": data["group"],
                "correo": data["email"],
                "puntaje_quiz": data["quiz_score"],
                "porcentaje": data["quiz_percentage"],
                "nivel_desempeno": data["level"],
                "reflexion_tiempo_real": data["real_time_reflection"],
                "reflexion_final": data["final_reflection"],
                "estrategia_usada": data["strategy"],
                "nodos_minimax": data["minimax_nodes"],
                "nodos_alphabeta": data["alphabeta_nodes"],
                "ramas_podadas": data["pruned"],
            }
        )
        st.session_state.csv_saved = True
    if st.session_state.csv_saved:
        st.success("Respuestas guardadas en respuestas_estudiantes.csv para ejecucion local.")


def main() -> None:
    init_state()
    inject_styles()
    render_student_registration()
    section = st.sidebar.radio("Navegacion", SECTIONS)
    st.sidebar.caption("Completa las secciones en orden para construir tu evidencia.")

    if not require_registration(section):
        render_home()
        return

    if section == "Inicio":
        render_home()
    elif section == "Conceptos clave":
        render_concepts()
    elif section == "Laboratorio interactivo":
        render_lab()
    elif section == "Comparacion Minimax vs Alfa-Beta":
        render_comparison()
    elif section == "Juegos con informacion imperfecta":
        render_imperfect_information()
    elif section == "Juegos en tiempo real":
        render_real_time()
    elif section == "Quiz formativo":
        render_quiz()
    elif section == "Evidencia y retroalimentacion final":
        render_evidence()


if __name__ == "__main__":
    main()
