import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QTextEdit, QPushButton, 
                            QGraphicsView, QGraphicsScene, QGraphicsTextItem)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QFont, QBrush, QColor, QPainter, QPen

from chess_parser import ChessGame
from chess_tree import ChessTreeVisualizer

#Abre la ventana dela aplicación
class MainWindow(QMainWindow):
   
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chess Game Parser and Visualizer")
        self.setGeometry(100, 100, 1200, 800)
        
        # Crea el diseño
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Panel izquierdo para el input
        left_panel = QVBoxLayout()
        
        self.input_label = QLabel("Enter Chess Game in SAN Notation:")
        left_panel.addWidget(self.input_label)
        
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText(
            "Example:\n1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 O-O"
        )
        left_panel.addWidget(self.input_text)
        
        self.parse_button = QPushButton("Parse and Visualize")
        self.parse_button.clicked.connect(self.parse_and_visualize)
        left_panel.addWidget(self.parse_button)
        
        self.error_display = QTextEdit()
        self.error_display.setReadOnly(True)
        self.error_display.setStyleSheet("""
            QTextEdit {
                color: #d32f2f;
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                padding: 5px;
                font-family: monospace;
            }
        """)
        left_panel.addWidget(self.error_display)
        
        # Panel derecho para el visualizador
        self.tree_visualizer = ChessTreeVisualizer()
        
        # Agrega los paneles al diseño principal
        main_layout.addLayout(left_panel, 1)
        main_layout.addWidget(self.tree_visualizer, 2)
    
    # Método para manejar el evento de clic en el botón "Parse and Visualize" (analizar y visualizar)
    def parse_and_visualize(self):
        # Obtiene el texto del input
        game_text = self.input_text.toPlainText()
        
        # Analiza el juego y valida movimientos
        chess_game = ChessGame()
        is_valid = chess_game.parse_game(game_text)
        
        # Muestra errores en el panel de errores
        # (si los hay) o limpia el panel si no hay errores
        if chess_game.errors:
            self.error_display.setPlainText("\n".join(chess_game.errors))
        else:
            self.error_display.clear()
        
        # Si el juego es válido, construye el árbol y lo visualiza
        if is_valid:
            root_node = chess_game.build_tree()
            self.tree_visualizer.visualize_tree(root_node)

#Ejecuta la aplicación
# (si este archivo se ejecuta directamente)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
