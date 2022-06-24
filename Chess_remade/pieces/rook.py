from chess_piece import ChessPiece


class Rook(ChessPiece):
    def identify_legal_moves(self, state):
        for r in (-1, 1):  # Row direction
            for s in range(8):  # Step size
                if state.clear_path_or_enemy(self.row, self.col, s*r, 0, self.col):
                    self.legal_moves.append(s*r, 0)
                else:
                    break
        for c in (-1, 1):  # Column direction
            for s in range(8):  # Step size
                if state.clear_path_or_enemy(self.row, self.col, 0, s*c, self.col):
                    self.legal_moves.append(0, s*c)
                else:
                    break
