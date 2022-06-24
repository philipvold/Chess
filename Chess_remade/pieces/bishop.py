from chess_piece import ChessPiece


class Bishop(ChessPiece):
    def identify_legal_moves(self, state):
        for s in range(8):  # Step-size
            for r in (-1, 1): # Row direction
                for c in (-1, 1):  # Column direction
                    if state.clear_path_or_enemy(self.row, self.col, s*r, s*c, self.color):
                        self.legal_moves.append(s*r, s*c)
