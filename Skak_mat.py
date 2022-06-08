# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


class Board(object):

    state = [
        ["X", "X", "X", "X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X", "X", "X", "X"],
        ["X", "X", "X", "X", "X", "X", "X", "X"],
    ]

    dead_pieces = []
    charged_pawns = {}
    moves = 0

    def reset_board(self):
        answer = input("Are you sure you want to reset the board? (y/n)").lower()
        while not answer in ["y", "n"]:
            print("That is not a valid answer")
            answer = input("Are you sure you want to reset the board? (y/n)").lower()
        if answer == "y":
            print("The board was reset!")
            self.state = [["X"] * 8] * 8
        else:
            print("Do not worry. We did not touch the board, Master.")

    def print_board(self):
        for field in self.state:
            print(
                field,
            )

    def change_field(self, new_status, row, col, setup=False):
        self.state[row][col] = new_status
        if not setup:
            self.moves += 1
            print("Move %s: %s to (%s,%s)" % (self.moves, new_status, row, col))


class Chesspiece(object):
    def __init__(self, color, name, board, setup=False):
        self.color = color
        self.name = name
        self.board = board

    def is_alive(self):
        if self.name in self.board.dead_pieces:
            return False
        else:
            return True


class Pawn(Chesspiece):
    def __init__(self, color, column, board, name):
        self.name = name
        self.board = board
        self.color = color
        self.column = column
        self.has_moved = False
        self.charged = 0

        if self.color == "W":
            self.row = 6
        elif self.color == "B":
            self.row = 1

        board.change_field(self.name, self.row, self.column, True)

    def move_piece(self, dest_row, dest_col):
        if self.legal_move(
            self.row, self.column, dest_row, dest_col, self.color, self.has_moved
        ):
            self.board.state[self.row][self.column] = "X"
            self.row = dest_row
            self.column = dest_col
            self.board.change_field(self.name, dest_row, dest_col)
            self.board.print_board()
            self.has_moved = True
            print()

    def legal_move(self, row, column, dest_row, dest_col, color, has_moved):
        if not self.is_alive():
            print("Master, that chesspiece is no longer with us. It has been slain.")
            return False
        elif not dest_row in range(0, 7) or not dest_col in range(0, 7):
            print("Sire, that is far beyond the realm of chess. I cannot do that!")
            return False
        elif (dest_row == self.row + 1 and self.color == "B") or (
            dest_row == self.row - 1 and self.color == "W"
        ):
            if abs(dest_col - self.column) == 0:
                if self.board.state[dest_row][dest_col] == "X":
                    return True
                else:
                    print("There is something in the way, Sire!")
                    return False
            elif abs(dest_col - self.column) == 1:
                if self.board.state[dest_row][dest_col] == "X":
                    if self.board.state[dest_row - 1][dest_col][:2] == "WP":
                        if (
                            self.board.moves
                            == self.board.charged_pawns[
                                self.board.state[dest_row - 1][dest_col]
                            ]
                        ):
                            self.board.dead_pieces.append(
                                self.board.state[dest_row - 1][dest_col]
                            )
                            self.board.state[dest_row - 1][dest_col] = "X"
                            print("En passant!")
                            return True
                        else:
                            print(
                                "Sire, while it seems possible to en passant, it would be ill advised. The enemy has been at the location for a while and has set up the proper defenses."
                            )
                            return False
                    elif self.board.state[dest_row + 1][dest_col][:2] == "BP":
                        if (
                            self.board.moves
                            == self.board.charged_pawns[
                                self.board.state[dest_row + 1][dest_col]
                            ]
                        ):
                            self.board.dead_pieces.append(
                                self.board.state[dest_row + 1][dest_col]
                            )
                            self.board.state[dest_row + 1][dest_col] = "X"
                            print("En passant!")
                            return True
                        else:
                            print(
                                "Sire, while it seems possible to en passant, it would be ill advised. The enemy has been at the location for a while and has set up the proper defenses."
                            )
                            return False
                    else:
                        print("Sire, there is no one to attack over there!")
                        return False
                elif self.board.state[dest_row][dest_col][0] == self.color:
                    print("Sire, I refuse to attack my trusted ally!")
                    return False
                else:
                    print("I will eliminate the enemy at once, Sire!")
                    self.board.dead_pieces.append(self.board.state[dest_row][dest_col])
                    return True
        elif (dest_row == self.row + 2 and self.color == "B") or (
            dest_row == self.row - 2 and self.color == "W"
        ):
            if not has_moved:
                if self.board.state[dest_row][dest_col] == "X" and (
                    (
                        self.board.state[dest_row - 1][dest_col] == "X"
                        and self.color == "B"
                    )
                    or (
                        self.board.state[dest_row + 1][dest_col] == "X"
                        and self.color == "W"
                    )
                ):
                    print("Chaaarge!")
                    self.charged = self.board.moves + 1
                    self.board.charged_pawns[self.name] = self.charged
                    return True
                else:
                    print("There is something in the way, Sire!")
                    return False
            else:
                print(
                    "I have already lost the element of surprise, Sire. I cannot charge from here."
                )
                return False
        else:
            print("I do not know how to do that, Sire!")
            return False


class Knight(Chesspiece):
    def __init__(self, color, column, board, name):
        self.name = name
        self.board = board
        self.color = color
        self.column = column

        if self.color == "W":
            self.row = 7
        elif self.color == "B":
            self.row = 0

        board.change_field(self.name, self.row, self.column, True)

    def move_piece(self, dest_row, dest_col):
        if self.legal_move(self.row, self.column, dest_row, dest_col, self.color):
            self.board.state[self.row][self.column] = "X"
            self.row = dest_row
            self.column = dest_col
            self.board.change_field(self.name, dest_row, dest_col)
            self.board.print_board()
            print()

    def legal_move(self, row, column, dest_row, dest_col, color):
        if not self.is_alive():
            print("Master, that chesspiece is no longer with us. It has been slain.")
            return False
        elif not dest_row in range(0, 7) or not dest_col in range(0, 7):
            print("Sire, that is far beyond the realm of chess. I cannot do that!")
            return False
        elif (
            abs(dest_col - self.column) in range(1, 3)
            and abs(dest_row - self.row) in range(1, 3)
            and abs(dest_col - self.column) != abs(dest_row - self.row)
        ):
            if self.board.state[dest_row][dest_col] == "X":
                return True
            elif self.board.state[dest_row][dest_col][0] == self.color:
                print("Sire, I refuse to attack my trusted ally!")
                return False
            else:
                print("I will eliminate the enemy at once, Sire!")
                self.board.dead_pieces.append(self.board.state[dest_row][dest_col])
                return True
        else:
            print("Sire, I cannot do that!")
            return False


""" Sets up the board """
""" Initialize the board itself """
BB = Board()

""" Ivory chesspieces """
WP0 = Pawn("W", 0, BB, "WP0")
WP1 = Pawn("W", 1, BB, "WP1")
WP2 = Pawn("W", 2, BB, "WP2")
WP3 = Pawn("W", 3, BB, "WP3")
WP4 = Pawn("W", 4, BB, "WP4")
WP5 = Pawn("W", 5, BB, "WP5")
WP6 = Pawn("W", 6, BB, "WP6")
WP7 = Pawn("W", 7, BB, "WP7")

WKn1 = Knight("W", 1, BB, "WKn1")
WKn2 = Knight("W", 6, BB, "WKn2")


""" Onyx chesspieces """
BP0 = Pawn("B", 0, BB, "BP0")
BP1 = Pawn("B", 1, BB, "BP1")
BP2 = Pawn("B", 2, BB, "BP2")
BP3 = Pawn("B", 3, BB, "BP3")
BP4 = Pawn("B", 4, BB, "BP4")
BP5 = Pawn("B", 5, BB, "BP5")
BP6 = Pawn("B", 6, BB, "BP6")
BP7 = Pawn("B", 7, BB, "BP7")

BKn1 = Knight("B", 1, BB, "BKn1")
BKn2 = Knight("B", 6, BB, "BKn2")

print("The chessboard has been set up, master!")
print()
print("Lets play chess!")
print()
BB.print_board()

BKn1.move_piece(2, 2)
BKn1.move_piece(4, 1)
BKn1.move_piece(6, 2)
WP2.move_piece(5, 2)
BKn1.move_piece(5, 4)
WP4.move_piece(5, 4)
WP5.move_piece(5, 4)
BKn1.move_piece(6, 2)
