from chess_piece import ChessPiece


class Knight(ChessPiece):
    def identify_legal_moves(self, state):
        for r in (-1, 1):  # Row direction
            for c in (-1, 1):  # Column direction
                for rs, cs in [(1, 2), (2, 1)]:  # Step-size in row and column
                    if state.empty_or_enemy(self.row, self.col, r * rs, c * cs, self.color):
                        self.legal_moves.append((r * rs, c * cs))
