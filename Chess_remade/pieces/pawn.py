" Implementation of pawns "

from chess_piece import ChessPiece


class Pawn(ChessPiece):
    
    def __init__(self, color, row, col, name):
        super().__init__(color, row, col, name)
        self.is_vulnerable = False
        
    def move(self, new_row, new_col):
        if self.moves == 0 and new_row == self.row + 2*self.color:
            self.is_vulnerable = True
        else:
            self.is_vulnerable = False
        super().move(new_row, new_col)
    
    def identify_legal_moves(self, state):
        # Use piece color to define direction
        direction = self.color
        
        if state.clear_path(self.row, self.col, direction, 0):
            self.legal_moves.append((direction, 0))
        
        # Can charge
        if self.moves == 0 and state.clear_path(self.row, self.col, direction * 2, 0):
            self.legal_moves.append((2*direction, 0))
            
        # Attacks
        for step in (-1, 1):
            if state.is_enemy(self.row + direction, self.col + step, self.color):
                self.legal_moves.append((direction, step))
                
        # # En passant
        # for step in (-1, 1):
        #     if board_state.is_enemy(self.row, self.col+step, self.color)
        
        
    