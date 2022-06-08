# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 19:45:20 2016

@author: Philip
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 13:02:55 2016

@author: Philip
"""


class AI2(object):
    def __init__(self, CB):
        self.board = CB

    def move(self, startRow, startCol, destRow, destCol):
        self.board.state[startRow][startCol].move_piece(destRow, destCol)

    def bent_move(self, startRow, startCol, destRow, destCol, mType):
        self.board.state[startRow][startCol].bent_move(destRow, destCol, mType)

    def bestMove(self, isWhite, branchBest, nRep=0):

        incumbent = [0, 0, 0, 0]

        if isWhite:
            color = "W"
            KC = self.board.white_moves
        else:
            color = "B"
            KC = self.board.black_moves

        if isWhite:
            incumbentScore = -1000
        else:
            incumbentScore = 1000

        """ Find possible moves """
        self.board.find_legal_moves()
        pieces = self.board.legal_moves[color].copy()
        for piece in pieces:
            SRow = piece.row
            SCol = piece.column
            legalMoves = pieces[piece]
            for legalMove in legalMoves:
                mType = legalMoves[legalMove]

                killed = self.getKilled(isWhite, mType, legalMove)

                """ Check if move actually legal by checking if board performs a move """
                self.bent_move(
                    piece.row, piece.column, legalMove[0], legalMove[1], mType
                )

                if not self.board.check[color]:
                    if nRep < 2:
                        score = self.bestMove(not isWhite, incumbentScore, nRep + 1)
                    else:
                        score = self.evaluateBoard()
                else:
                    """ If move is illegal return bad scores """
                    if isWhite:
                        score = -10000
                    else:
                        score = 10000

                self.board.reverseMove(
                    piece, SRow, SCol, legalMove[0], legalMove[1], mType, KC, killed
                )
                if nRep > 0:
                    if isWhite:
                        if score > branchBest:
                            return score
                    else:
                        if score < branchBest:
                            return score

                if isWhite:
                    if score > incumbentScore:
                        incumbentScore = score
                        incumbent = [SRow, SCol, legalMove[0], legalMove[1]]
                else:
                    if score < incumbentScore:
                        incumbentScore = score
                        incumbent = [
                            piece.row,
                            piece.column,
                            legalMove[0],
                            legalMove[1],
                        ]

        if nRep > 0:
            return incumbentScore

        if nRep == 0:
            print(incumbent, incumbentScore)
            return incumbent

    def getKilled(self, isWhite, mType, legalMove):
        if mType != "passant":
            killed = self.board.state[legalMove[0]][legalMove[1]]
        else:
            if isWhite:
                killed = self.board.state[legalMove[0] + 1][legalMove[1]]
            else:
                killed = self.board.state[legalMove[0] - 1][legalMove[1]]
        return killed

    def evaluateBoard(self):
        result = 0
        result += self.materialScore()
        result += self.moveScore()
        result += self.pawnPosition()
        return result

    def pawnPosition(self):
        result = 0
        pawns = self.getPawns()
        cols = self.pawnColumns(pawns)
        result += self.isolatedPawns(cols)
        # result += self.doubledPawns(cols)
        return result

    def pawnColumns(self, pawns):
        wcols = [P.column for P in pawns[0]]
        bcols = [P.column for P in pawns[1]]

        Cols = []

        for i in range(8):
            Cols.append((i, wcols.count(i), bcols.count(i)))
        return Cols

    def materialScore(self):
        result = 0

        """ Evaluate score for living pieces """
        for piece in self.board.is_alive["W"]:
            result += self.pieceScore(piece)
        for piece in self.board.is_alive["B"]:
            result -= self.pieceScore(piece)
        return result

    def moveScore(self):
        result = 0
        for piece in self.board.legal_moves["W"]:
            result += len(self.board.legal_moves["W"][piece])
        for piece in self.board.legal_moves["B"]:
            result -= len(self.board.legal_moves["B"][piece])
        return 0.1 * result

    def isolatedPawns(self, columns):
        result = 0
        for i in range(8):
            if i in range(1, 7):
                if (
                    columns[i][1] > 0
                    and columns[i + 1][1] == 0
                    and columns[i - 1][1] == 0
                ):
                    result -= 0.5
                if (
                    columns[i][2] > 0
                    and columns[i + 1][2] == 0
                    and columns[i - 1][1] == 0
                ):
                    result += 0.5
            elif i == 0:
                if columns[i][1] > 0 and columns[i + 1][1] == 0:
                    result -= 0.5
                if columns[i][2] > 0 and columns[i + 1][2] == 0:
                    result += 0.5
            else:
                if columns[i][1] > 0 and columns[i - 1][1] == 0:
                    result -= 0.5
                if columns[i][2] > 0 and columns[i - 1][2] == 0:
                    result += 0.5
        return result

    def getPawns(self):
        pawns = [[], []]

        for piece in self.board.is_alive["W"]:
            if piece.Ctype[1] == "P":
                pawns[0].append(piece)
        for piece in self.board.is_alive["B"]:
            if piece.Ctype[1] == "P":
                pawns[1].append(piece)
        return pawns

    def pieceScore(self, piece):
        pType = piece.Ctype[1:]
        if pType == "P":
            return 1
        elif pType in ["K", "B"]:
            return 3
        elif pType == "R":
            return 5
        elif pType == "Qn":
            return 9
        else:
            return 200
