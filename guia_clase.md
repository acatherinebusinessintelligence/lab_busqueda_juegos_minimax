
# Guía rápida de clase

## Unidad 3: Búsqueda en juegos

### Laboratorio: ¿Cómo decide una IA frente a un adversario?

### Momento 1. Activación

Pregunta inicial:

> Si una IA juega contra ti, ¿decide solo por la jugada actual o también por las respuestas futuras del adversario?

### Momento 2. Demostración

El docente abre la aplicación y muestra:

- Tablero de Tres en Raya
- Jugador humano
- Jugador IA
- Estrategia Minimax
- Estrategia Alfa-Beta
- Nodos explorados
- Ramas podadas

### Momento 3. Comparación

Los estudiantes deben observar:

| Elemento | Minimax | Alfa-Beta |
|---|---|---|
| ¿Encuentra buena jugada? | Sí | Sí |
| ¿Explora todos los nodos posibles? | Sí | No |
| ¿Reduce costo computacional? | No | Sí |
| ¿Cambia la decisión final? | No necesariamente | No, si se aplica correctamente |

### Momento 4. Reto

Modificar el código para responder:

1. ¿Qué pasa si ganar vale 10 en lugar de 1?
2. ¿Qué pasa si perder penaliza con -5?
3. ¿Qué pasa si se prefiere ganar en menos turnos?
4. ¿Qué pasaría si el juego fuera más grande?

### Momento 5. Cierre

Lección aprendida:

> En juegos competitivos, un agente inteligente no decide solamente por lo que quiere lograr, sino por lo que anticipa que el adversario hará para impedirlo.
