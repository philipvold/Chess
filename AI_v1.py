# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 13:02:55 2016

@author: Philip
"""

import SkakMat2 as SM
import copy


class AI1(object):
    def __init__(self, CB):
        self.board = CB

    def move(self, startRow, startCol, destRow, destCol):
        self.board.state[startRow][startCol].move_piece(destRow, destCol)

    def randomLegalMove(self):
        if self.board.wt:
            color = "W"
        else:
            color = "B"
        finalmove = [0, 0, 0, 0]
        for piece in self.board.legal_moves[color]:
            for move in self.board.legal_moves[color][piece]:
                finalmove = [piece.row, piece.column, move[0], move[1]]
        self.board.aidanMoves.append(self.board.moves)
        if __name__ == "__main__":
            self.move(finalmove[0], finalmove[1], finalmove[2], finalmove[3])
        return finalmove

    def best_move(self, counter=0):
        if self.board.wt:
            color = "W"
        else:
            color = "B"
        best = [0, 0, 0, 0]
        bestscore = -1000
        for piece in self.board.legal_moves[color]:
            for move in self.board.legal_moves[color][piece]:
                mscore = self.moveScore(piece, move, counter)
                if mscore >= bestscore:
                    best = [piece.row, piece.column, move[0], move[1]]
                    bestscore = mscore
        if counter == 2:
            print("Aidan moves: ", best, " with score ", bestscore)
        self.board.aidanMoves.append(self.board.moves)
        return best

    def moveScore(self, piece, move, counter=0):
        movetype = self.board.legal_moves[piece.color][piece][move]
        piecetype = piece.Ctype
        result = 0
        if piecetype in ["WP", "BP"] and move[0] in [0, 7]:
            result += 8.0
        if (
            self.board.moves <= 8
            and piecetype == ["WK"]
            and move in [(5, 2), (5, 5), (6, 3), (6, 4)]
            or piecetype == ["BK"]
            and move in [(2, 2), (2, 5), (1, 3), (1, 4)]
        ):
            result += 0.2
        if movetype == "ordinary":
            if piecetype in ["WKi", "BKi"]:
                result -= 0.01
            result += 0.1

        elif movetype == "attack":
            killtype = self.board.state[move[0]][move[1]].Ctype[1:]
            if killtype == "P":
                result += 1.01
            elif killtype in ["B", "K"]:
                result += 3.01
            elif killtype == "R":
                result += 5.01
            elif killtype == "Qn":
                result += 9.01
            elif killtype == "Ki":
                return 900.0
        elif movetype in ["long castling", "short castling"]:
            result += 5.00
        elif movetype == "charge":
            result += 0.15
        elif movetype == "passant":
            result += 0.5
        if counter > 0:
            counter -= 1
            result -= self.evaluate_counter(piece, move, counter)
        return result

    def evaluate_counter(self, piece, move, counter):
        tester = copy.deepcopy(self)
        copied_board = tester.board
        copied_board.name = "Tester"
        copied_board.aidanMoves.append(copied_board.moves)
        copy_piece = copied_board.state[piece.row][piece.column]
        if not copy_piece.move_piece(move[0], move[1]):
            return 1000.0
        else:
            copied_board.wt = not copied_board.wt
            counterMove = tester.best_move(counter)
            counterPiece = copied_board.state[counterMove[0]][counterMove[1]]
            counterScore = tester.moveScore(
                counterPiece, (counterMove[2], counterMove[3]), 0
            )
            return counterScore - 0.1


Aidan = AI1(SM.Board())
