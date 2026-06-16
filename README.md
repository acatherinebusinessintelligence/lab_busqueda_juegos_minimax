# OVA Unidad 3: Busqueda en juegos y agentes adversarios

Aplicacion educativa interactiva en Streamlit para la Unidad 3 de Inteligencia Artificial. El proyecto transforma un laboratorio de Tres en Raya en un OVA de clase centrado en juego contra IA, explicacion inmediata de cada decision y evidencia de aprendizaje descargable.

## Objetivo academico

Master class: **Jugadas Inteligentes: Estrategias Optimas en Juegos a traves de la Busqueda**.

El laboratorio busca analizar como la busqueda en juegos sigue siendo un area activa, con desafios como exploracion eficiente, informacion imperfecta, decisiones en tiempo real e integracion con tecnicas de aprendizaje automatico.

## Resultado de aprendizaje

El estudiante analiza y aplica algoritmos de busqueda en juegos, considerando aspectos como la complejidad, la eficiencia y la optimizacion.

## Estructura de la app

- `Inicio`: presentacion del modulo, objetivo, resultado de aprendizaje y registro del estudiante.
- `Conceptos clave`: definiciones, ejemplos en Tres en Raya y preguntas rapidas con retroalimentacion.
- `Laboratorio interactivo`: nucleo de la app. El estudiante juega como O contra la IA X, recibe analisis de su movimiento, pensamiento del agente, opciones evaluadas, concepto aprendido e historial de jugadas.
- `Comparacion Minimax vs Alfa-Beta`: cuadro comparativo, metricas y grafico de nodos explorados.
- `Juegos con informacion imperfecta`: comparacion entre ajedrez, poker, Tres en Raya y decisiones simultaneas.
- `Juegos en tiempo real`: explicacion de profundidad limitada, heuristicas y restricciones de tiempo.
- `Quiz formativo`: minimo 10 preguntas con retroalimentacion automatica y nivel de desempeno.
- `Evidencia y retroalimentacion final`: resumen, reflexion final, descarga Markdown y registro CSV local.

## Archivos principales

- `app.py`: interfaz Streamlit y flujo del OVA.
- `game_logic.py`: reglas de Tres en Raya, Minimax, Poda Alfa-Beta y analisis de jugadas.
- `quiz_data.py`: conceptos clave y preguntas del quiz.
- `utils.py`: calculo de desempeno, generacion de evidencia y guardado CSV.
- `requirements.txt`: dependencias para ejecucion local y Streamlit Cloud.
- `guia_clase.md`: guia rapida para uso docente.

## Instalacion local

```bash
git clone URL_DEL_REPOSITORIO
cd lab_busqueda_juegos_minimax
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

En macOS o Linux, activa el entorno con:

```bash
source .venv/bin/activate
```

## Ejecucion

```bash
streamlit run app.py
```

La aplicacion no requiere rutas absolutas ni archivos externos adicionales.

## Despliegue desde GitHub

1. Sube estos archivos a un repositorio de GitHub.
2. Entra a Streamlit Cloud.
3. Selecciona el repositorio.
4. Configura `app.py` como archivo principal.
5. Verifica que `requirements.txt` este en la raiz del proyecto.
6. Despliega la aplicacion.

## Recomendacion para Streamlit Cloud

La descarga de evidencia en Markdown es la opcion recomendada para recoger entregables de estudiantes en despliegues en la nube. Streamlit Cloud puede permitir escritura temporal, pero no debe asumirse persistencia permanente del archivo `respuestas_estudiantes.csv`.

Para uso local en laboratorio o computador docente, el boton **Guardar respuestas en CSV local** crea o actualiza `respuestas_estudiantes.csv` con los datos del estudiante, resultado del quiz, reflexiones, estrategia usada y metricas del laboratorio.

## Actividad sugerida para estudiantes

1. Completa el registro inicial.
2. Recorre los conceptos clave y responde las preguntas de comprension.
3. Juega una partida usando Minimax.
4. Reinicia el tablero y juega usando Poda Alfa-Beta.
5. En cada turno revisa el analisis del movimiento, el pensamiento del agente y la tabla de opciones evaluadas.
6. Usa el boton **Comparar algoritmos en este tablero** para revisar mejor jugada, nodos, ramas podadas y ahorro aproximado.
7. Responde la actividad de juegos en tiempo real.
8. Presenta el quiz formativo.
9. Escribe la reflexion final y descarga la evidencia Markdown con historial y explicaciones.

## Posibles mejoras futuras

- Agregar visualizacion grafica parcial del arbol de juego.
- Incluir profundidad limitada configurable.
- Agregar heuristicas editables por el estudiante.
- Crear modo IA vs IA.
- Ampliar el laboratorio a Conecta 4 simplificado.
- Integrar almacenamiento persistente con Google Sheets, una base de datos o un LMS.
