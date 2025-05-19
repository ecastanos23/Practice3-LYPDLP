# Practice3-LYPDLP

# Análisis sintáctico del juego de Ajedrez con visualización de turnos a través de árbol binario. 

## Vista de la práctica 
Este proyecto implementa un programa en Python que valida sintácticamente partidas de ajedrez escritas en Notación Algebraica Estándar (SAN) y las represente visualmente como un árbol binario de jugadas por turnos.

## Funcionalidades 

### Validación Sintáctica
Verifica que cada movimiento cumpla con las reglas SAN según la gramática BNF proporcionada.

### Visualización de Árbol Binario
Genera una representación gráfica de la partida donde:

- Cada nodo raíz representa un turno.
- Los hijos izquierdos son jugadas blancas.
- Los hijos derechos son jugadas negras.

### Manejo de errores
Detecta y reporta movimientos inválidos con mensajes descriptivos.

## Correr el código 

### Requisitos
- Pyhton 3.8+
- Bibliotecas requeridas: pip install PyQt5

## Estructura del proyecto
/practica_III/
│── chess_parser.py       # Clases principales ChessMove, ChessTurn y ChessGame

│── chess_tree.py         # Clase ChessTreeVisualizer

│── chess_gui.py          # Clase MainWindow (interfaz gráfica)

│── test_games/           # Ejemplos de partidas
│   ├── valid_game.san
│   └── invalid_game.san
└── README.md

└── README.md

## Gramática implementada 
<partida> ::= { <turno> }

<turno> ::= <numero_turno> "." <jugada_blanca> [<jugada_negra>]

<jugada> ::= <enroque> | <movimiento_pieza> | <movimiento_peon>

<enroque> ::= "O-O" | "O-O-O"

<movimiento_pieza> ::= <pieza> <desambiguacion>? <captura>? <casilla>

<movimiento_peon> ::= <peon_captura> | <peon_avance>

<pieza> ::= "K" | "Q" | "R" | "B" | "N"

<casilla> ::= <letra><numero>

## Ejemplo de uso

1. Ejecutar la interfaz gráfica:
   python chess_gui.py
2. Ingresar una partida en SAN:
   1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7
3. El programa mostrará:
   - Errores de sintaxis (si existen)
   - Árbol binario interactivo de la partida válida
  
## Equipo 
- Estudiante 1: Emmanuel Castaño Sepúlveda.
- Estudiante 2: Jerónimo Contreras. 

## Video
  



