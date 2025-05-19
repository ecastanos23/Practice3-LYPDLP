
# modulo para trabajar con expresiones regulares
import re
# modulo para trabajar con la interfaz grafica

#Clase para representar y validar un movimiento de ajedrez
class ChessMove:
    #Representa y valida un movimiento de ajedrez en notación SAN
    def __init__(self, move_text, is_white=True):
        # Inicializa el movimiento de ajedrez
        self.move_text = move_text.strip()
        # Indica si el movimiento es de una pieza blanca o negra
        # (True para blanca, False para negra)
        self.is_white = is_white
        self.is_valid = False
        # Lista para almacenar errores de validación
        # (por ejemplo, formato inválido)
        self.validation_errors = []
        self.validate()
        
    #Validar el movimiento contra las reglas estándar de notación algebraica
    def validate(self):
        
        if not self.move_text:
            # Si el movimiento está vacío, se considera inválido
            self.validation_errors.append("Empty move")
            return
        
        #Remover simbolos de jaque o jaque mate para la validación
        san_move = self.move_text.rstrip('+#')
        
        #Verificar enroque (movimiento especial donde el rey y la torre cambian de lugar en un mismo movimiento)
        # Enroque corto (O-O) o enroque largo (O-O-O)
        if re.fullmatch(r'^(O-O|O-O-O)$', san_move):
            self.is_valid = True
            return
        
        #Verificar el movimiento de la pieza (rey, reina, torre, alfil, caballo)
        # (K, Q, R, B, N)
      
        piece_pattern = r'^([KQRBN])([a-h]?[1-8]?)x?([a-h][1-8])(=[QRBN])?$'
        if re.fullmatch(piece_pattern, san_move):
            self.is_valid = True
            return
        
        # Verificar el movimiento de un peón
        pawn_pattern = r'^([a-h]?)x?([a-h][1-8])(=[QRBN])?$'
        if re.fullmatch(pawn_pattern, san_move):
            self.is_valid = True
            return
        
        # Si el movimiento no coincide con ninguna de las reglas anteriores, es inválido
        self.validation_errors.append(f"Invalid move format: {self.move_text}")

#Validar el turno de ajedrez

class ChessTurn:
    #Representa un turno de ajedrez con un movimiento blanco y opcionalmente un movimiento
    def __init__(self, turn_number, white_move, black_move=None):
        # Inicializa el turno de ajedrez
        self.turn_number = turn_number
        # Inicializa el movimiento blanco
        self.white_move = ChessMove(white_move, is_white=True)
        # Inicializa el movimiento negro (si existe)
        self.black_move = ChessMove(black_move, is_white=False) if black_move else None
    
    
    def is_valid(self):
       #Verificar si ambos movimientos en el turno son válidos
        if not self.white_move.is_valid:
            return False
        if self.black_move and not self.black_move.is_valid:
            return False
        return True
    
    def get_errors(self):
        ##Retornar todos los errores de validación en este turno
        errors = []
        if not self.white_move.is_valid:
            errors.append(f"Turn {self.turn_number} white move: {', '.join(self.white_move.validation_errors)}")
        if self.black_move and not self.black_move.is_valid:
            errors.append(f"Turn {self.turn_number} black move: {', '.join(self.black_move.validation_errors)}")
        return errors

#Clase para representar el juego de ajedrez y construir el árbol binario
class ChessGame:

    def __init__(self):
         #Contiene una lista de turnos y errores
        self.turns = []
        self.errors = []
        #Nodo raíz del árbol binario
        self.tree_root = None
    
    #Método para analizar el texto del juego y validar los movimientos
    # (en formato SAN) y construir el árbol binario
    def parse_game(self, game_text):
        # Inicializa la lista de turnos y errores
        self.turns = []
        self.errors = []
        
        # Normaliza el texto del juego (elimina espacios innecesarios)
        # y elimina comentarios (entre llaves)
        game_text = ' '.join(game_text.split())
        game_text = re.sub(r'\{.*?\}', '', game_text)  # Remove {comments}
        
        # Elimina los números de los turnos (1., 2., etc.) y los espacios
        turn_pattern = r'(\d+)\.\s*([^\s]+)\s*([^\s]*)'
        # Busca los turnos en el texto del juego
        # y los almacena en la lista de turnos
        turns = re.findall(turn_pattern, game_text)
        
        # Itera sobre los turnos encontrados
        # y crea objetos ChessTurn para cada uno
        for turn in turns:
            turn_num, white_move, black_move = turn
            black_move = black_move if black_move else None
            chess_turn = ChessTurn(turn_num, white_move, black_move)
            self.turns.append(chess_turn)
            # Verifica si el turno es válido
            # y agrega errores a la lista de errores
            if not chess_turn.is_valid():
                self.errors.extend(chess_turn.get_errors())
        
        # Verifica si hay algun texto no analizado
        # que no coincide con el patrón de turnos
        remaining = re.sub(turn_pattern, '', game_text).strip()
        if remaining:
            self.errors.append(f"Invalid format in remaining text: {remaining}")
        
        return len(self.errors) == 0
    
    #Método para construir el árbol binario a partir de los turnos
    # y sus movimientos
    def build_tree(self):
        #Construye el árbol binario a partir de los turnos

        if self.errors:
            return None
        
        # Clase interna para representar un nodo del árbol
      
        class TreeNode:
            #Representa un nodo del árbol binario
            # (cada nodo representa un movimiento de ajedrez)
            def __init__(self, data, is_white=True, parent=None):
                self.data = data
                self.is_white = is_white
                self.left = None
                self.right = None
                self.parent = parent
                self.x = 0
                self.y = 0
        
        # Inicializa el nodo raíz del árbol
        # (representa el inicio de la partida)
        self.tree_root = TreeNode("Partida", is_white=True)
        current_parent = self.tree_root
        
        # Itera sobre los turnos y construye el árbol binario
        # (cada turno tiene un movimiento blanco y opcionalmente un movimiento negro)
        for turn in self.turns:
            #Movimiento blanco (left child)
            white_node = TreeNode(
                f"{turn.turn_number}. {turn.white_move.move_text}",
                is_white=True,
                parent=current_parent
            )
            current_parent.left = white_node
            
            #Movimiento negro (right child si existe)
            if turn.black_move:
                black_node = TreeNode(
                    turn.black_move.move_text,
                    is_white=False,
                    parent=current_parent
                )
                current_parent.right = black_node
                current_parent = black_node   #Ir al nodo negro del siguiente turno 
            else:
                current_parent = white_node #Ir al nodo blanco si no hay movimiento de negro
        return self.tree_root
