import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QTextEdit, QPushButton, 
                            QGraphicsView, QGraphicsScene, QGraphicsTextItem)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QFont, QBrush, QColor, QPainter, QPen
# Visualizar el arbol binario con respectivos colores (blanco y negro)
class ChessTreeVisualizer(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.node_radius = 40
        self.level_height = 100
        self.horizontal_spacing = 80
        self.setMinimumSize(800, 600)
        
        # Definicion de colores 
        self.white_color = QColor(240, 240, 255)   #Color claro para blancos
        self.black_color = QColor(50, 50, 70)      #Color oscuro para negros 
        self.white_text = QColor(10, 10, 10)       #Color de texto oscuro para movimientos blancos 
        self.black_text = QColor(240, 240, 240)    #Color de texto negro para movimientos negros
        self.white_line = QColor(150, 150, 150)    #Linea gris para movimientos blancos
        self.black_line = QColor(80, 80, 80)       #Linea gris oscura para movimientos negros
    
    #Dibuja el arbol binario comenzando desde el nodo raíz 
    def visualize_tree(self, root_node):
        self.scene.clear()
        if not root_node:
            return
        
        #Calcula la posición y dibuja los nodos
        self._calculate_positions(root_node, 0, 0)
        self._draw_tree(root_node)
        
        #Centra la vista del arbol
        self.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
    
    #Caclula las posiciones de todos los nodos
    def _calculate_positions(self, node, level, pos):
        if not node:
            return 0
        
        left_width = self._calculate_positions(node.left, level + 1, pos)
        node.x = pos + left_width + self.horizontal_spacing
        node.y = level * self.level_height
        right_width = self._calculate_positions(node.right, level + 1, node.x + self.node_radius)
        
        return left_width + right_width + self.horizontal_spacing
    
    #Dibuja los nodos y las conexiones entre ellos
    # (recursivamente)
    def _draw_tree(self, node):
        if not node:
            return
        
        #Establece el color del nodo basado en el tipo de movimiento (blanco / negro)
        if node.is_white:
            node_brush = QBrush(self.white_color)
            text_color = self.white_text
            line_color = self.white_line
        else:
            node_brush = QBrush(self.black_color)
            text_color = self.black_text
            line_color = self.black_line
        
        # Dibuja el nodo
        pen = QPen(Qt.black, 1)
        ellipse = self.scene.addEllipse(
            node.x - self.node_radius, 
            node.y - self.node_radius,
            self.node_radius * 2, 
            self.node_radius * 2,
            pen,
            node_brush
        )
        
        text = self.scene.addText(node.data)
        text.setDefaultTextColor(text_color)
        text.setPos(
            node.x - text.boundingRect().width()/2, 
            node.y - text.boundingRect().height()/2
        )
        font = QFont("Arial", 9)
        text.setFont(font)
        
        #Dibuja la conexion al nodo left child (movimiento blanco)
        if node.left:
            line = self.scene.addLine(
                node.x, node.y + self.node_radius,
                node.left.x, node.left.y - self.node_radius,
                QPen(line_color, 1.5))
            line.setZValue(-1)
            self._draw_tree(node.left)
        
        # Dibuja la conexion al right child (movimiento negro)
        if node.right:
            line = self.scene.addLine(
                node.x, node.y + self.node_radius,
                node.right.x, node.right.y - self.node_radius,
                QPen(line_color, 1.5))
            line.setZValue(-1)
            self._draw_tree(node.right)
