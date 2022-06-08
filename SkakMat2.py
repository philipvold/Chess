# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


class Board(object):
    def __init__(self):
        self.name = "Main"
        
        self.state = []
        self.is_alive = {}
        self.is_dead = {}
        self.legal_moves = {}
        self.black_moves = 50
        self.white_moves = 50
        
        self.charged_pawns = {}
        self.moves = 0
        self.recalculate_moves = 0
        self.aidanMoves = []
        self.betaBentMove = False
        self.check = {"W": False, "B": False}
        
        self.start()
        self.setup_board()
        self.find_legal_moves()
        self.wt = True
    
    def start(self):
        """ Initializes the internal board state. """
        self.state = [[None for r in range(8)] for c in range(8)]
        
        self.is_alive = {"B": [], "W": []}
        self.is_dead = {"B": [], "W": []}
        self.legal_moves = {"B": {}, "W": {}}
        
        self.black_moves = 50
        self.white_moves = 50
        
        self.charged_pawns = {}
        self.moves = 0
        self.recalculate_moves = 0
        self.aidanMoves = []
        self.betaBentMove = False
        self.check = {"W": False, "B": False}
    
    def reset_board(self):
        """ Resets the board after a confirmatory prompt. """
        answer = input("Are you sure you want to reset the board? (y/n)").lower()
        while not answer in ["y", "n"]:
            print("That is not a valid answer")
            answer = input("Are you sure you want to reset the board? (y/n)").lower()
        if answer == "y":
            print("The board was reset!")
            self.start()
            self.setup_board()
        else:
            print("Do not worry. We did not touch the board, Master.")
    
    def print_board(self):
        for row in self.state:
            output = []
            for item in row:
                if item is not None:
                    output.append(item.name)
                else:
                    output.append("XXX")
            print("  ".join(output))
        print("\n")
    
    def clear_path(self, row, column, dest_row, dest_col):
        """ Checks if fields in between current position and destination are empty """
        if dest_row in range(0, 8) and dest_col in range(0, 8):
            if row != dest_row and column != dest_col:
                if not abs(row - dest_row) == abs(column - dest_col):
                    print("Master, that move is neither straight nor diagonal!")
                    return False
                else:
                    if dest_col > column and dest_row > row:
                        for i in range(1, dest_row - row):
                            if self.state[row + i][column + i] is not None:
                                return False
                        else:
                            return True
                    if dest_col > column and dest_row < row:
                        for i in range(1, dest_col - column):
                            if self.state[row - i][column + i] is not None:
                                return False
                        else:
                            return True
                    if dest_col < column and dest_row > row:
                        for i in range(1, dest_row - row):
                            if self.state[row + i][column - i] is not None:
                                return False
                        else:
                            return True
                    if dest_col < column and dest_row < row:
                        for i in range(1, row - dest_row):
                            if self.state[row - i][column - i] is not None:
                                return False
                        else:
                            return True
            elif row != dest_row and column == dest_col:
                for i in range(min(1, dest_row - row + 1), max(0, dest_row - row)):
                    if self.state[row + i][column] is not None:
                        return False
                else:
                    return True
            elif row == dest_row and column != dest_col:
                for i in range(min(1, dest_col - column + 1), max(0, dest_col - column)):
                    if self.state[row][column + i] is not None:
                        return False
                else:
                    return True
            else:
                return False
    
    def kill_piece(self, dest_row, dest_col):
        piece = self.state[dest_row][dest_col]
        if isinstance(piece, Chesspiece):
            self.is_alive[piece.color].remove(piece)
            self.is_dead[piece.color].append(piece)
            self.state[piece.row][piece.column] = None
            piece.is_alive = False
    
    def unkill_piece(self, piece, dest_row, dest_col):
        self.is_dead[piece.color].remove(piece)
        self.is_alive[piece.color].append(piece)
        self.state[dest_row][dest_col] = piece
        piece.is_alive = True
    
    def find_legal_moves(self):
        for color in ["B", "W"]:
            self.legal_moves[color] = {}
            for item in self.is_alive[color]:
                self.legal_moves[color][item] = {}
                item.legal_moves()
    
    def convert(self, piece):
        row = piece.row
        column = piece.column
        name = piece.name
        clr = piece.color
        self.kill_piece(row, column)
        if not self.moves - 1 in self.aidanMoves and not self.betaBentMove:
            ctype = input("Well done, Master! What kind of piece would you like? (Rook, Knight, Bishop, Queen)")
            while ctype not in ["Rook", "Knight", "Bishop", "Queen"]:
                ctype = input("Well done, Master! What kind of piece would you like? (Rook, Knight, Bishop, Queen)")
        else:
            ctype = "Queen"
        
        if ctype == "Queen":
            self.item = self.place_piece(Queen, clr, row, column, clr + "Qn-" + name)
        elif ctype == "Knight":
            self.item = self.place_piece(Knight, clr, row, column, clr + "K-" + name)
        elif ctype == "Rook":
            self.item = self.place_piece(Rook, clr, row, column, clr + "R-" + name)
        else:
            self.item = self.place_piece(Bishop, clr, row, column, clr + "B-" + name)
    
    def reverseMove(self, piece, SRow, SCol, ERow, ECol, moveType, kingCount, killed):
        if moveType in ["ordinary", "charge"]:
            self.reverseOrdinaryMove(SRow, SCol, ERow, ECol)
        elif moveType == "attack":
            self.reverseAttack(SRow, SCol, ERow, ECol, killed)
        elif moveType in ["long castling", "short castling"]:
            self.uncastle(piece, moveType)
        elif moveType == "passant":
            self.unpassant(SRow, SCol, ERow, ECol, killed)
        
        if piece.color == "W":
            self.white_moves += kingCount
        else:
            self.black_moves += kingCount
        piece.moves -= 1
        self.moves -= 1
    
    def reverseOrdinaryMove(self, SRow, SCol, ERow, ECol):
        piece = self.state[ERow][ECol]
        piece.place_piece(SRow, SCol)
        piece.remove_piece(ERow, ECol)
    
    def reverseAttack(self, SRow, SCol, ERow, ECol, killed):
        self.reverseOrdinaryMove(SRow, SCol, ERow, ECol)
        self.unkill_piece(killed, killed.row, killed.column)
    
    def castle(self, piece, dest_row, dest_col):
        if dest_row == 7:
            if dest_col == 2:
                self.state[7][0].bent_move(7, 3, "ordinary")
            else:
                self.state[7][7].bent_move(7, 5, "ordinary")
        else:
            if dest_col == 2:
                self.state[0][0].bent_move(0, 3, "ordinary")
            else:
                self.state[0][7].bent_move(0, 5, "ordinary")
    
    def uncastle(self, piece, moveType):
        if piece.color == "W":
            if moveType == "long castling":
                self.reverseOrdinaryMove(7, 4, 7, 2)
                self.reverseOrdinaryMove(7, 0, 7, 3)
                self.state[7][0].moves = 0
            else:
                self.reverseOrdinaryMove(7, 4, 7, 6)
                self.reverseOrdinaryMove(7, 7, 7, 5)
                self.state[7][7].moves = 0
        else:
            if moveType == "long castling":
                self.reverseOrdinaryMove(0, 4, 0, 2)
                self.reverseOrdinaryMove(0, 0, 0, 3)
                self.state[0][0].moves = 0
            else:
                self.reverseOrdinaryMove(0, 4, 0, 6)
                self.reverseOrdinaryMove(0, 7, 0, 5)
                self.state[0][7].moves = 0
    
    def passant(self, piece, dest_row, dest_col):
        if piece.color == "W":
            self.kill_piece(dest_row + 1, dest_col)
        else:
            self.kill_piece(dest_row - 1, dest_col)
    
    def unpassant(self, SRow, SCol, ERow, ECol, killed):
        self.reverseOrdinaryMove(SRow, SCol, ERow, ECol)
        self.unkill_piece(killed, killed.row, killed.column)
    
    def place_piece(self, piece, color, row, column, name):
        return piece(color, row, column, name, self)
    
    def setup_board(self):
        """ Ivory chesspieces """
        self.WP0 = self.place_piece(Pawn, "W", 6, 0, "WP0")
        self.WP1 = self.place_piece(Pawn, "W", 6, 1, "WP1")
        self.WP2 = self.place_piece(Pawn, "W", 6, 2, "WP2")
        self.WP3 = self.place_piece(Pawn, "W", 6, 3, "WP3")
        self.WP4 = self.place_piece(Pawn, "W", 6, 4, "WP4")
        self.WP5 = self.place_piece(Pawn, "W", 6, 5, "WP5")
        self.WP6 = self.place_piece(Pawn, "W", 6, 6, "WP6")
        self.WP7 = self.place_piece(Pawn, "W", 6, 7, "WP7")
        
        self.WR1 = self.place_piece(Rook, "W", 7, 0, "WR1")
        self.WR2 = self.place_piece(Rook, "W", 7, 7, "WR2")
        
        self.WK1 = self.place_piece(Knight, "W", 7, 1, "WK1")
        self.WK2 = self.place_piece(Knight, "W", 7, 6, "WK2")
        
        self.WB1 = self.place_piece(Bishop, "W", 7, 2, "WB1")
        self.WB2 = self.place_piece(Bishop, "W", 7, 5, "WB2")
        
        self.WQn = self.place_piece(Queen, "W", 7, 3, "WQn")
        
        self.WKi = self.place_piece(King, "W", 7, 4, "WKi")
        
        """ Onyx chesspieces """
        self.BP0 = self.place_piece(Pawn, "B", 1, 0, "BP0")
        self.BP1 = self.place_piece(Pawn, "B", 1, 1, "BP1")
        self.BP2 = self.place_piece(Pawn, "B", 1, 2, "BP2")
        self.BP3 = self.place_piece(Pawn, "B", 1, 3, "BP3")
        self.BP4 = self.place_piece(Pawn, "B", 1, 4, "BP4")
        self.BP5 = self.place_piece(Pawn, "B", 1, 5, "BP5")
        self.BP6 = self.place_piece(Pawn, "B", 1, 6, "BP6")
        self.BP7 = self.place_piece(Pawn, "B", 1, 7, "BP7")
        
        self.BR1 = self.place_piece(Rook, "B", 0, 0, "BR1")
        self.BR2 = self.place_piece(Rook, "B", 0, 7, "BR2")
        
        self.BK1 = self.place_piece(Knight, "B", 0, 1, "BK1")
        self.BK2 = self.place_piece(Knight, "B", 0, 6, "BK2")
        
        self.BB1 = self.place_piece(Bishop, "B", 0, 2, "BB1")
        self.BB2 = self.place_piece(Bishop, "B", 0, 5, "BB2")
        
        self.BQn = self.place_piece(Queen, "B", 0, 3, "BQn")
        
        self.BKi = self.place_piece(King, "B", 0, 4, "BKi")


class Chesspiece(object):
    def __init__(self, color, row, column, name, board):
        self.color = color
        self.row = row
        self.column = column
        self.name = name
        self.board = board
        self.moves = 0
        
        self.is_alive = True
        
        board.is_alive[self.color].append(self)
        board.legal_moves[self.color][self] = {}
        
        self.place_piece(self.row, self.column)
        
        self.Ctype = self.ctp()
    
    def ctp(self):
        return self.name[:2]
    
    shouts = {"ordinary": "", "attack": "I shall eliminate the enemy at once, Sire!",
        "friendlyfire": "Sire, I refuse to attack my trusted ally!", "charge": "Chaaarge!!", "passant": "En passant!",
        "castling": "The fortifications have been built, Sire", "check": "Sire, we have the enemy king in check!",
        "checkmate": "Sire, we have captured the enemy king! Victory is ours!", }
    
    def reset_king_count(self):
        if self.color == "B":
            self.board.black_moves = 50
        else:
            self.board.white_moves = 50
    
    def bent_move(self, dest_row, dest_col, m_type):
        
        if m_type in ["short castling", "long castling"]:
            self.board.castle(self, dest_row, dest_col)
        elif m_type == "passant":
            self.board.passant(self, dest_row, dest_col)
        
        self.board.kill_piece(dest_row, dest_col)
        self.remove_piece(self.row, self.column)
        self.place_piece(dest_row, dest_col)
        
        self.board.find_legal_moves()
        
        self.board.check["W"] = self.board.WKi.in_check()
        self.board.check["B"] = self.board.BKi.in_check()
        
        self.board.moves += 1
        self.moves += 1
    
    def move_piece(self, dest_row, dest_col):
        if self.is_alive is False:
            print("Master, that piece died in combat.")
            return False
        elif (dest_row, dest_col) in self.board.legal_moves[self.color][self]:
            killed = self.board.state[dest_row][dest_col]
            startrow = self.row
            startcol = self.column
            moveset = self.board.legal_moves[self.color][self]
            mtype = moveset[(dest_row, dest_col)]
            
            if self.color == "W":
                k_c = self.board.white_moves
            else:
                k_c = self.board.black_moves
            
            self.board.kill_piece(dest_row, dest_col)
            self.remove_piece(self.row, self.column)
            self.place_piece(dest_row, dest_col)
            
            self.row = dest_row
            self.column = dest_col
            if self.board.recalculate_moves != self.board.moves:
                self.board.find_legal_moves()
            if self.color == "W":
                incheck = self.board.WKi.in_check()
            else:
                incheck = self.board.BKi.in_check()
            
            self.moves += 1
            self.board.moves += 1
            
            if not incheck:
                if mtype in ["short castling", "long castling"]:
                    if self.color == "W":
                        if mtype == "long castling":
                            rk = self.board.state[7][0]
                            rk.place_piece(7, 3)
                            rk.row = 7
                            rk.column = 3
                            rk.remove_piece(7, 0)
                        else:
                            rk = self.board.state[7][7]
                            rk.place_piece(7, 5)
                            rk.row = 7
                            rk.column = 5
                            rk.remove_piece(7, 7)
                    else:
                        if mtype == "long castling":
                            rk = self.board.state[0][0]
                            rk.place_piece(0, 3)
                            rk.row = 0
                            rk.column = 3
                            rk.remove_piece(0, 0)
                        else:
                            rk = self.board.state[0][7]
                            rk.place_piece(0, 5)
                            rk.row = 0
                            rk.column = 5
                            rk.remove_piece(0, 7)
                if self.color == "W":
                    self.board.white_moves -= 1
                else:
                    self.board.black_moves -= 1
                
                if self.name[1:2] == "P":
                    self.reset_king_count()
                    if self.row == 0:
                        self.board.convert(self)
                    if self.row == 7:
                        self.board.convert(self)
                    if moveset[(dest_row, dest_col)] == "passant":
                        if self.color == "W":
                            self.board.kill_piece(dest_row + 1, dest_col)
                        else:
                            self.board.kill_piece(dest_row - 1, dest_col)
                
                self.board.find_legal_moves()
                return True
            else:
                if (not self.board.betaBentMove and not self.board.moves - 1 in self.board.aidanMoves):
                    print("That move leaves our king unprotected!")
                self.board.reverseMove(self, startrow, startcol, dest_row, dest_col, mtype, k_c, killed)
                self.board.recalculate_moves = self.board.moves
                return False
        else:
            print("Illegal move")
        return False
    
    def place_piece(self, row, column):
        self.board.state[row][column] = self
        self.row = row
        self.column = column
    
    def remove_piece(self, row, column):
        self.board.state[row][column] = None


class Pawn(Chesspiece):
    def legal_moves(self):
        if not self.row in [0, 7]:
            if self.color == "W":
                if self.board.state[self.row - 1][self.column] is None:
                    self.board.legal_moves[self.color][self][(self.row - 1, self.column)] = "ordinary"
                    if self.moves == 0:
                        if self.board.clear_path(self.row, self.column, self.row - 3, self.column):
                            self.board.legal_moves[self.color][self][(self.row - 2, self.column)] = "charge"
                            self.board.charged_pawns[self] = self.board.moves
                if (self.column - 1 >= 0 and self.board.state[self.row - 1][self.column - 1] is not None):
                    if self.board.state[self.row - 1][self.column - 1].name[:1] == "B":
                        self.board.legal_moves[self.color][self][(self.row - 1, self.column - 1)] = "attack"
                if (self.column + 1 <= 7 and self.board.state[self.row - 1][self.column + 1] is not None):
                    if self.board.state[self.row - 1][self.column + 1].name[:1] == "B":
                        self.board.legal_moves[self.color][self][(self.row - 1, self.column + 1)] = "attack"
                if self.row == 3:
                    if (self.column - 1 >= 0 and self.board.state[self.row - 1][self.column - 1] is None and
                            self.board.state[self.row][self.column - 1] is not None):
                        opp = self.board.state[self.row][self.column - 1]
                        if (opp.name[1:2] == "P" and opp.moves == 1 and self.board.charged_pawns[
                            opp] == self.board.moves - 1):
                            self.board.legal_moves[self.color][self][(self.row - 1, self.column - 1)] = "passant"
                    if (self.column + 1 <= 7 and self.board.state[self.row - 1][self.column + 1] is None and
                            self.board.state[self.row][self.column + 1] is not None):
                        opp = self.board.state[self.row][self.column + 1]
                        if (opp.name[1:2] == "P" and opp.moves == 1 and self.board.charged_pawns[
                            opp] == self.board.moves - 1):
                            self.board.legal_moves[self.color][self][(self.row - 1, self.column + 1)] = "passant"
            else:
                if self.board.state[self.row + 1][self.column] is None:
                    self.board.legal_moves[self.color][self][(self.row + 1, self.column)] = "ordinary"
                    if self.moves == 0:
                        if self.board.clear_path(self.row, self.column, self.row + 3, self.column):
                            self.board.legal_moves[self.color][self][(self.row + 2, self.column)] = "charge"
                            self.board.charged_pawns[self] = self.board.moves
                if (self.column - 1 >= 0 and self.board.state[self.row + 1][self.column - 1] is not None):
                    if self.board.state[self.row + 1][self.column - 1].name[:1] == "W":
                        self.board.legal_moves[self.color][self][(self.row + 1, self.column - 1)] = "attack"
                if (self.column + 1 <= 7 and self.board.state[self.row + 1][self.column + 1] is not None):
                    if self.board.state[self.row + 1][self.column + 1].name[:1] == "W":
                        self.board.legal_moves[self.color][self][(self.row + 1, self.column + 1)] = "attack"
                if self.row == 4:
                    if (self.column - 1 >= 0 and self.board.state[self.row + 1][self.column - 1] is None and
                            self.board.state[self.row][self.column - 1] is not None):
                        opp = self.board.state[self.row][self.column - 1]
                        if (opp.name[1:2] == "P" and opp.moves == 1 and self.board.charged_pawns[
                            opp] == self.board.moves - 1):
                            self.board.legal_moves[self.color][self][(self.row + 1, self.column - 1)] = "passant"
                    if (self.column + 1 <= 7 and self.board.state[self.row + 1][self.column + 1] is None and
                            self.board.state[self.row][self.column + 1] is not None):
                        opp = self.board.state[self.row][self.column + 1]
                        if (opp.name[1:2] == "P" and opp.moves == 1 and self.board.charged_pawns[
                            opp] == self.board.moves - 1):
                            self.board.legal_moves[self.color][self][(self.row + 1, self.column + 1)] = "passant"


class Rook(Chesspiece):
    def legal_moves(self):
        destinations = [(self.row, col) for col in range(8)]
        destinations += [(row, self.column) for row in range(8)]
        
        for row, col in destinations:
            target = self.board.state[row][col]
            
            if target and self.board.clear_path(self.row, self.column, row, col):
                m_type = "ordinary" if target.color != self.color else "attack"
                self.board.legal_moves[self.color][self][(row, col)] = m_type


class Knight(Chesspiece):
    def legal_moves(self):
        if self.column + 2 <= 7 and self.row + 1 <= 7:
            dest = self.board.state[self.row + 1][self.column + 2]
            if dest is None:
                self.board.legal_moves[self.color][self][(self.row + 1, self.column + 2)] = "ordinary"
            elif dest.color != self.color:
                self.board.legal_moves[self.color][self][(self.row + 1, self.column + 2)] = "attack"
        if self.column + 2 <= 7 and self.row - 1 >= 0:
            dest = self.board.state[self.row - 1][self.column + 2]
            if dest is None:
                self.board.legal_moves[self.color][self][(self.row - 1, self.column + 2)] = "ordinary"
            elif dest.color != self.color:
                self.board.legal_moves[self.color][self][(self.row - 1, self.column + 2)] = "attack"
        if self.column + 1 <= 7 and self.row + 2 <= 7:
            dest = self.board.state[self.row + 2][self.column + 1]
            if dest is None:
                self.board.legal_moves[self.color][self][(self.row + 2, self.column + 1)] = "ordinary"
            elif dest.color != self.color:
                self.board.legal_moves[self.color][self][(self.row + 2, self.column + 1)] = "attack"
        if self.column + 1 <= 7 and self.row - 2 >= 0:
            dest = self.board.state[self.row - 2][self.column + 1]
            if dest is None:
                self.board.legal_moves[self.color][self][(self.row - 2, self.column + 1)] = "ordinary"
            elif dest.color != self.color:
                self.board.legal_moves[self.color][self][(self.row - 2, self.column + 1)] = "attack"
        if self.column - 2 >= 0 and self.row + 1 <= 7:
            dest = self.board.state[self.row + 1][self.column - 2]
            if dest is None:
                self.board.legal_moves[self.color][self][(self.row + 1, self.column - 2)] = "ordinary"
            elif dest.color != self.color:
                self.board.legal_moves[self.color][self][(self.row + 1, self.column - 2)] = "attack"
        if self.column - 2 >= 0 and self.row - 1 >= 0:
            dest = self.board.state[self.row - 1][self.column - 2]
            if dest is None:
                self.board.legal_moves[self.color][self][(self.row - 1, self.column - 2)] = "ordinary"
            elif dest.color != self.color:
                self.board.legal_moves[self.color][self][(self.row - 1, self.column - 2)] = "attack"
        if self.column - 1 >= 0 and self.row + 2 <= 7:
            dest = self.board.state[self.row + 2][self.column - 1]
            if dest is None:
                self.board.legal_moves[self.color][self][(self.row + 2, self.column - 1)] = "ordinary"
            elif dest.color != self.color:
                self.board.legal_moves[self.color][self][(self.row + 2, self.column - 1)] = "attack"
        if self.column - 1 >= 0 and self.row - 2 >= 0:
            dest = self.board.state[self.row - 2][self.column - 1]
            if dest is None:
                self.board.legal_moves[self.color][self][(self.row - 2, self.column - 1)] = "ordinary"
            elif dest.color != self.color:
                self.board.legal_moves[self.color][self][(self.row - 2, self.column - 1)] = "attack"


class Bishop(Chesspiece):
    def legal_moves(self):
        for i in range(-7, 7):
            if i + self.row in range(0, 8) and i + self.column in range(0, 8):
                dest = self.board.state[self.row + i][self.column + i]
                if self.board.clear_path(self.row, self.column, self.row + i, self.column + i):
                    if dest is None:
                        self.board.legal_moves[self.color][self][(self.row + i, self.column + i)] = "ordinary"
                    elif dest.color != self.color:
                        self.board.legal_moves[self.color][self][(self.row + i, self.column + i)] = "attack"
            if self.row + i in range(0, 8) and self.column - i in range(0, 8):
                dest = self.board.state[self.row + i][self.column - i]
                if self.board.clear_path(self.row, self.column, self.row + i, self.column - i):
                    if dest is None:
                        self.board.legal_moves[self.color][self][(self.row + i, self.column - i)] = "ordinary"
                    elif dest.color != self.color:
                        self.board.legal_moves[self.color][self][(self.row + i, self.column - i)] = "attack"


class Queen(Chesspiece):
    def ctp(self):
        return self.name[:3]
    
    def legal_moves(self):
        """ Diagonal moves from bishop"""
        for i in range(-7, 7):
            if i + self.row in range(0, 8) and i + self.column in range(0, 8):
                dest = self.board.state[self.row + i][self.column + i]
                if self.board.clear_path(self.row, self.column, self.row + i, self.column + i):
                    if dest is None:
                        self.board.legal_moves[self.color][self][(self.row + i, self.column + i)] = "ordinary"
                    elif dest.color != self.color:
                        self.board.legal_moves[self.color][self][(self.row + i, self.column + i)] = "attack"
            if self.row + i in range(0, 8) and self.column - i in range(0, 8):
                dest = self.board.state[self.row + i][self.column - i]
                if self.board.clear_path(self.row, self.column, self.row + i, self.column - i):
                    if dest is None:
                        self.board.legal_moves[self.color][self][(self.row + i, self.column - i)] = "ordinary"
                    elif dest.color != self.color:
                        self.board.legal_moves[self.color][self][(self.row + i, self.column - i)] = "attack"
        """ Horizontal and vertical moves from rook"""
        for cols in range(0, 8):
            dest = self.board.state[self.row][cols]
            if dest is None:
                if self.board.clear_path(self.row, self.column, self.row, cols) is True:
                    self.board.legal_moves[self.color][self][(self.row, cols)] = "ordinary"
            elif dest.color != self.color:
                if self.board.clear_path(self.row, self.column, self.row, cols) is True:
                    self.board.legal_moves[self.color][self][(self.row, cols)] = "attack"
        for rows in range(0, 8):
            dest = self.board.state[rows][self.column]
            if dest is None:
                if (self.board.clear_path(self.row, self.column, rows, self.column) == True):
                    self.board.legal_moves[self.color][self][(rows, self.column)] = "ordinary"
            elif dest.color != self.color:
                if (self.board.clear_path(self.row, self.column, rows, self.column) == True):
                    self.board.legal_moves[self.color][self][(rows, self.column)] = "attack"


class King(Chesspiece):
    def ctp(self):
        return self.name[:3]
    
    def legal_moves(self):
        mincol = self.column - 1
        maxcol = self.column + 1
        minrow = self.row - 1
        maxrow = self.row + 1
        if self.column == 0:
            mincol = 0
        elif self.column == 7:
            maxcol = 7
        if self.row == 0:
            minrow = 0
        elif self.row == 7:
            maxrow = 7
        
        for i in range(minrow, maxrow + 1):
            for j in range(mincol, maxcol + 1):
                if self.board.state[i][j] is None:
                    self.board.legal_moves[self.color][self][(i, j)] = "ordinary"
                elif self.board.state[i][j].color != self.color:
                    self.board.legal_moves[self.color][self][(i, j)] = "attack"
        """ Castling """
        if self.moves == 0 and not self.in_check():
            if self.color == "W":
                if self.board.WR2.moves == 0 and self.board.clear_path(7, 4, 7, 7):
                    for item in self.board.legal_moves["B"]:
                        if (7, 5) in self.board.legal_moves["B"][item] or (7, 6,) in self.board.legal_moves["B"][item]:
                            break
                    else:
                        self.board.legal_moves[self.color][self][(7, 6)] = "short castling"
                if self.board.WR1.moves == 0 and self.board.clear_path(7, 4, 7, 0):
                    for item in self.board.legal_moves["B"]:
                        if (7, 2) in self.board.legal_moves["B"][item] or (7, 3,) in self.board.legal_moves["B"][item]:
                            break
                    else:
                        self.board.legal_moves[self.color][self][(7, 2)] = "long castling"
            else:
                if self.board.BR2.moves == 0 and self.board.clear_path(0, 4, 0, 7):
                    for item in self.board.legal_moves["W"]:
                        if (0, 5) in self.board.legal_moves["W"][item] or (0, 6,) in self.board.legal_moves["W"][item]:
                            break
                    else:
                        self.board.legal_moves[self.color][self][(0, 6)] = "short castling"
                if self.board.BR1.moves == 0 and self.board.clear_path(0, 4, 0, 0):
                    for item in self.board.legal_moves["W"]:
                        if (0, 3) in self.board.legal_moves["W"][item] or (0, 2,) in self.board.legal_moves["W"][item]:
                            break
                    else:
                        self.board.legal_moves[self.color][self][(0, 2)] = "long castling"
    
    def in_check(self):
        if self.color == "W":
            oppcol = "B"
        else:
            oppcol = "W"
        
        for item in self.board.legal_moves[oppcol]:
            if (self.row, self.column) in self.board.legal_moves[oppcol][item]:
                return True
        else:
            return False
