"""
    Base class of all chess pieces.

"""


class ChessPiece:
    def __init__(self, color, row, col, name):
        self.color = color
        self.row = row
        self.col = col
        
        self.last_col = self.col
        self.last_row = self.row
        
        self.name = name
        self.moves = 0
        self.in_play = True
        
        self.legal_moves = []
        
    def move(self, new_row, new_col):
        self.last_row, self.last_col = self.row, self.col
        self.row, self.col = new_row, new_col
        self.moves += 1
        
    def reverse_move(self):
        self.row, self.col = self.last_row, self.last_col
        self.moves -= 1
    
    def kill(self):
        self.in_play = False
        self.row, self.col = None, None
        
    def identify_legal_moves(self, state):
        pass
